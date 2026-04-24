/**
 * content.js — YouTuDo (Client-Server Version)
 * Interroge l'API Python locale au lieu de parser le DOM.
 */

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'GET_FORMATS') {
    const videoUrl = window.location.href;
    const apiUrl = `http://127.0.0.1:8000/api/info?url=${encodeURIComponent(videoUrl)}`;
    
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => sendResponse(data))
      .catch(err => {
        console.error("YouTuDo API Error:", err);
        sendResponse({ success: false, error: 'Serveur API Python non accessible. Assurez-vous que le backend tourne sur le port 8000.' });
      });
      
    // Retourne true pour indiquer une réponse asynchrone
    return true;
  }
});


