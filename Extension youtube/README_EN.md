<div align="center">
  <p>
    <a href="README.md">Français</a> | 
    <a href="README_EN.md">English</a> | 
    <a href="README_ZH.md">中文</a> | 
    <a href="README_ES.md">Español</a> | 
    <a href="README_RU.md">Русский</a> | 
    <a href="README_DE.md">Deutsch</a>
  </p>
  <h1>✨ YouTuDo</h1>
  <p><strong>The Premium YouTube Download Extension</strong></p>
</div>

---

**YouTuDo** is a browser extension coupled with a powerful local server. It allows you to extract and download YouTube videos (including **4K**) with any audio track, smartly bypassing security measures and speed throttling.

## ⚠️ System Requirements (PC)

To function optimally, YouTuDo needs a small local "engine". Ensure you have installed the following:

| Software | Description & Download Link |
| :--- | :--- |
| 🐍 **Python 3** | Required to run the local API server.<br>🔗 **[Download Python](https://www.python.org/downloads/windows/)** |
| 🟩 **Node.js** | **Crucial.** Decrypts YouTube's anti-bot protections to download at maximum speed. *(Must be installed in its default folder: `C:\Program Files\nodejs`)*.<br>🔗 **[Download Node.js (LTS Version)](https://nodejs.org/)** |
| 🎬 **FFmpeg** | **Essential.** Cutting-edge tool that merges 4K video streams with your chosen audio. *(The executable must be added to your Windows `PATH`)*.<br>🔗 **[Download FFmpeg (Windows Builds)](https://www.gyan.dev/ffmpeg/builds/)** or via [GitHub](https://github.com/BtbN/FFmpeg-Builds/releases) |
| 🌐 **Browser** | A Chromium-based browser (Google Chrome, Microsoft Edge, Brave, etc.). |

---

## ⚙️ Setup Guide

### 1️⃣ Configure the Local Server (Backend)
The server does the heavy lifting in the background (extraction and merging).

1. Open a terminal (Command Prompt or PowerShell) in the `youtube-api` folder.
2. Install the necessary Python dependencies by typing:
   ```cmd
   pip install fastapi uvicorn yt-dlp
   ```
3. Start the server:
   ```cmd
   python -m uvicorn main:app --reload
   ```
   > 💡 **Tip:** Leave this terminal open. The server will automatically check for `yt-dlp` updates (the core downloader) in the background every time it starts!

### 2️⃣ Install the Extension (Frontend)
1. Open your browser and go to the extensions management page (type `chrome://extensions/` or `edge://extensions/` in the address bar).
2. Enable **"Developer mode"** (usually a toggle in the top right corner).
3. Click the **"Load unpacked"** button.
4. Select the extension's root folder (the main folder containing the `manifest.json` file).

---

## 🚀 Daily Usage

1. **Preparation**: Make sure your Python server (`main.py`) is running.
2. **Navigation**: Go to the YouTube video page of your choice.
3. **Selection**: Click the YouTuDo extension icon in your toolbar. The interface will open and load all available formats (including hidden audio dubs).
4. **Download**: Choose the resolution or audio track you like and start the download with a single click!

> ⚠️ **Important Note:** Do not close your terminal window while a video is downloading, otherwise the operation will be cancelled.
