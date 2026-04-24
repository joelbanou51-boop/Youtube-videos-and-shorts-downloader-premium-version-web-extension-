/**
 * background.js — YouTuDo (Persistent Polling)
 */

let state = { activeTaskId: null, status: 'idle', progress: 0, speed: '', filename: '', error: null };

chrome.storage.local.get(['ytd_state'], (res) => {
    if (res.ytd_state) {
        state = res.ytd_state;
        if (state.activeTaskId && (state.status === 'downloading' || state.status === 'merging')) {
            startPolling(state.activeTaskId);
        }
    }
});

function saveState() { chrome.storage.local.set({ ytd_state: state }); }
function broadcastState() { chrome.runtime.sendMessage({ type: 'JOB_UPDATE', state }); }

let pollingInterval = null;

function startPolling(taskId) {
    if (pollingInterval) clearInterval(pollingInterval);
    pollingInterval = setInterval(async () => {
        try {
            const res = await fetch(`http://127.0.0.1:8000/api/download/status/${taskId}`);
            const data = await res.json();
            Object.assign(state, data); // Met à jour status, progress, speed, filename, etc.
            saveState();
            broadcastState();
            if (['finished', 'error', 'cancelled'].includes(data.status)) {
                stopPolling();
                if (data.status === 'finished') triggerDownload(taskId, data.filename);
            }
        } catch (e) { console.error("Polling error", e); }
    }, 1000);
}

function stopPolling() { clearInterval(pollingInterval); pollingInterval = null; }

function triggerDownload(taskId, filename) {
    chrome.downloads.download({ url: `http://127.0.0.1:8000/api/download/file/${taskId}`, filename: filename || 'video.mp4', saveAs: false });
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.type === 'START_JOB') {
        const { url, format_id, merge_id } = msg.payload;
        fetch('http://127.0.0.1:8000/api/download/start', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, format_id, merge_id })
        })
        .then(r => r.json()).then(data => {
            if (data.success) {
                state = { activeTaskId: data.task_id, status: 'downloading', progress: 0, speed: '', filename: '', error: null };
                saveState();
                startPolling(data.task_id);
                sendResponse({ success: true });
            } else sendResponse({ success: false, error: data.error });
        }).catch(e => sendResponse({ success: false, error: e.message }));
        return true;
    }
    if (msg.type === 'CANCEL_JOB' && state.activeTaskId) {
        fetch(`http://127.0.0.1:8000/api/download/cancel/${state.activeTaskId}`, { method: 'POST' }).then(() => {
            state.status = 'cancelled'; saveState(); stopPolling(); broadcastState();
        });
    }
    if (msg.type === 'GET_CURRENT_STATE') sendResponse(state);
    if (msg.type === 'RESET_JOB') {
        state = { activeTaskId: null, status: 'idle', progress: 0, speed: '', filename: '', error: null };
        saveState(); broadcastState();
    }
});
