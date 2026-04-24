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
  <p><strong>高级 YouTube 下载扩展</strong></p>
</div>

---

**YouTuDo** 是一个浏览器扩展，配备了强大的本地服务器。它可以让您提取和下载 YouTube 视频（包括 **4K**）及任何音轨，并智能绕过安全保护和限速。

## ⚠️ 系统要求 (PC)

为了达到最佳运行效果，YouTuDo 需要一个本地“引擎”。请确保您已安装以下组件：

| 软件 | 描述与下载链接 |
| :--- | :--- |
| 🐍 **Python 3** | 运行本地 API 服务器所必需。<br>🔗 **[下载 Python](https://www.python.org/downloads/windows/)** |
| 🟩 **Node.js** | **至关重要。** 用于解密 YouTube 的反机器人保护，从而以最高速度下载。*(必须安装在默认文件夹中：`C:\Program Files\nodejs`)*.<br>🔗 **[下载 Node.js (LTS 版本)](https://nodejs.org/)** |
| 🎬 **FFmpeg** | **不可或缺。** 用于将 4K 视频流与您选择的音频合并。*(该执行文件必须添加到 Windows 的 `PATH` 环境变量中)*.<br>🔗 **[下载 FFmpeg (Windows 版本)](https://www.gyan.dev/ffmpeg/builds/)** 或通过 [GitHub](https://github.com/BtbN/FFmpeg-Builds/releases) |
| 🌐 **浏览器** | 基于 Chromium 的浏览器（Google Chrome、Microsoft Edge、Brave 等）。 |

---

## ⚙️ 安装指南

### 1️⃣ 配置本地服务器 (后端)
服务器负责在后台处理繁重的工作（提取和合并）。

1. 在 `youtube-api` 文件夹中打开一个终端（命令提示符或 PowerShell）。
2. 输入以下命令安装必要的 Python 依赖项：
   ```cmd
   pip install fastapi uvicorn yt-dlp
   ```
3. 启动服务器：
   ```cmd
   python -m uvicorn main:app --reload
   ```
   > 💡 **提示：** 请保持此终端打开。每次启动时，服务器都会在后台自动检查 `yt-dlp`（核心下载器）的更新！

### 2️⃣ 安装扩展 (前端)
1. 打开浏览器并进入扩展管理页面（在地址栏中输入 `chrome://extensions/` 或 `edge://extensions/`）。
2. 启用 **“开发者模式”**（通常是右上角的开关）。
3. 点击 **“加载已解压的扩展程序”** (Load unpacked) 按钮。
4. 选择扩展的根文件夹（包含 `manifest.json` 文件的主要文件夹）。

---

## 🚀 日常使用

1. **准备**：确保您的 Python 服务器 (`main.py`) 正在运行。
2. **浏览**：转到您选择的 YouTube 视频页面。
3. **选择**：点击工具栏中的 YouTuDo 扩展图标。界面将打开并加载所有可用格式（包括隐藏的配音音轨）。
4. **下载**：选择您喜欢的视频分辨率或音轨，一键开始下载！

> ⚠️ **重要提示：** 视频下载时请勿关闭终端窗口，否则操作将被取消。
