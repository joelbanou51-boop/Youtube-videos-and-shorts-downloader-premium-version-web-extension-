/**
 * popup.js — YouTuDo
 * Version Synchronisée avec Jobs + Bords Arrondis.
 */

let allFormats = [], videoTitle = '', channelName = '', activeFilter = 'all', tab = null;
const $ = id => document.getElementById(id);

// DOM
const loadingState = $('loadingState'), errorState = $('errorState'), errorMessage = $('errorMessage');
const mainContent = $('mainContent'), videoTitleEl = $('videoTitle'), videoInfoEl = $('videoInfo');
const filterTabs = $('filterTabs'), formatListEl = $('formatList');
const progressOverlay = $('progressOverlay'), progressText = $('progressText'), progressBar = $('progressBar');
const progressPercent = $('progressPercent'), videoThumbnailEl = $('videoThumbnail');
const videoDurationBadge = $('videoDurationBadge'), cancelBtn = $('cancelBtn');

document.addEventListener('DOMContentLoaded', init);

async function init() {
  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
  tab = activeTab;

  chrome.runtime.sendMessage({ type: 'GET_CURRENT_STATE' }, (state) => {
    if (state && state.activeTaskId && !['idle', 'finished', 'cancelled'].includes(state.status)) {
        updateUIFromState(state);
    } else {
        loadFormats();
    }
  });

  chrome.runtime.onMessage.addListener((msg) => {
    if (msg.type === 'JOB_UPDATE') updateUIFromState(msg.state);
  });

  if (cancelBtn) cancelBtn.addEventListener('click', () => chrome.runtime.sendMessage({ type: 'CANCEL_JOB' }));
  
  if (filterTabs) {
    filterTabs.addEventListener('click', (e) => {
      const t = e.target.closest('.tab');
      if (!t || t.dataset.filter === activeFilter) return;
      document.querySelectorAll('.tab').forEach(x => x.classList.remove('tab--active'));
      t.classList.add('tab--active');
      activeFilter = t.dataset.filter;
      renderFormats();
    });
  }
}

function loadFormats() {
  if (!tab || !(tab.url?.includes('youtube.com/watch') || tab.url?.includes('youtube.com/shorts'))) {
    showError('Ouvrez une vidéo YouTube.'); return;
  }
  chrome.tabs.sendMessage(tab.id, { type: 'GET_FORMATS' }, (res) => {
    if (chrome.runtime.lastError || !res?.success) { showError(res?.error || 'Erreur formats.'); return; }
    allFormats = res.formats; videoTitle = res.videoTitle; channelName = res.channelName;
    videoTitleEl.innerHTML = channelName ? `<b>${channelName}</b> — ${videoTitle}` : videoTitle;
    videoInfoEl.classList.add('visible');
    if (res.thumbnail) videoThumbnailEl.src = res.thumbnail;
    if (res.duration) { videoDurationBadge.textContent = formatDuration(res.duration); videoDurationBadge.classList.remove('hidden'); }
    showMain(); renderFormats();
  });
}

function renderFormats() {
  const formats = activeFilter === 'all' ? allFormats : allFormats.filter(f => f.type === activeFilter);
  formatListEl.innerHTML = '';
  const bestAudio = findBestAudio();
  formats.forEach(f => formatListEl.appendChild(buildFormatCard(f, bestAudio)));
}

function buildFormatCard(fmt, bestAudio) {
  const card = document.createElement('div');
  card.className = 'format-card';
  card.innerHTML = `
    <span class="quality-badge ${getBadgeClass(fmt)}">${getLabel(fmt)}</span>
    <div class="format-info">
      <div class="format-info__main">${buildMainLabel(fmt)}</div>
      <div class="format-info__sub"><span class="type-badge type-${fmt.type}">${getTypeLabel(fmt)}</span><span>${formatBytes(fmt.filesize)}</span></div>
    </div>
    <button class="btn-download"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zm-14 10v2h14v-2H5z"/></svg></button>
  `;
  card.querySelector('.btn-download').onclick = () => {
    chrome.runtime.sendMessage({ type: 'START_JOB', payload: { url: tab.url, format_id: fmt.itag, merge_id: fmt.type === 'video-only' ? bestAudio?.itag : null }});
  };
  return card;
}

function updateUIFromState(state) {
    if (state.status === 'idle') { hideProgress(); return; }
    const labels = { downloading: `Téléchargement (${state.speed})...`, merging: 'Fusion Finalisation...', finished: 'Terminé ! ✅', cancelled: 'Annulé 🛑', error: 'Erreur ❌' };
    showProgress(labels[state.status] || state.status, state.progress);
    if (['finished', 'cancelled', 'error'].includes(state.status)) {
        setTimeout(() => { chrome.runtime.sendMessage({ type: 'RESET_JOB' }); hideProgress(); loadFormats(); }, 3000);
    }
}

// Helpers
function findBestAudio() { return allFormats.filter(f => f.type === 'audio-only').sort((a,b) => (b.filesize||0)-(a.filesize||0))[0]; }
function formatBytes(b) { if(!b) return ''; return b < 1048576 ? (b/1024).toFixed(0)+' Ko' : (b/1048576).toFixed(1)+' Mo'; }
function getLabel(f) { return f.qualityLabel || (f.type==='audio-only'?'Audio':'?'); }
function getBadgeClass(f) { if(f.type==='audio-only') return 'badge--audio'; const h=f.height||0; return h>=2160?'badge--4k':h>=1080?'badge--1080':'badge--low'; }
function buildMainLabel(f) { if(f.type==='audio-only'){ const lang = f.languageName || f.language; const l=lang&&lang!=='und'?' ['+lang.toUpperCase()+']':''; const abr = f.abr ? ` (${Math.round(f.abr)}kbps)` : ''; return f.container+' Audio'+l+abr; } return (f.qualityLabel||f.height+'p')+' — '+f.container; }
function getTypeLabel(f) {
  if (f.type === 'video-only') return '⚡ Fusion auto';
  if (f.type === 'muxed') return '✓ Vidéo+Audio';
  return '♪ Audio seul';
}
function formatDuration(s) { return Math.floor(s/60)+':'+String(s%60).padStart(2,'0'); }
function showMain() { loadingState.classList.add('hidden'); errorState.classList.add('hidden'); mainContent.classList.remove('hidden'); }
function showError(m) { loadingState.classList.add('hidden'); mainContent.classList.add('hidden'); errorState.classList.remove('hidden'); errorMessage.textContent=m; }
function showProgress(t, p) { progressOverlay.classList.remove('hidden'); progressText.textContent = t; progressBar.style.width = p+'%'; progressPercent.textContent = Math.round(p)+'%'; }
function hideProgress() { progressOverlay.classList.add('hidden'); }
