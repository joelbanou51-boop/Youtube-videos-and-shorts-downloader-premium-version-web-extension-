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
  <p><strong>Die Premium YouTube-Download-Erweiterung</strong></p>
</div>

---

**YouTuDo** ist eine Browser-Erweiterung in Kombination mit einem leistungsstarken lokalen Server. Sie ermöglicht es Ihnen, YouTube-Videos (einschließlich **4K**) mit jeder gewünschten Audiospur zu extrahieren und herunterzuladen, wobei Sicherheitsmaßnahmen und Drosselungen intelligent umgangen werden.

## ⚠️ Systemanforderungen (PC)

Um optimal zu funktionieren, benötigt YouTuDo einen kleinen lokalen "Motor". Stellen Sie sicher, dass Sie Folgendes installiert haben:

| Software | Beschreibung & Download-Link |
| :--- | :--- |
| 🐍 **Python 3** | Erforderlich, um den lokalen API-Server auszuführen.<br>🔗 **[Python herunterladen](https://www.python.org/downloads/windows/)** |
| 🟩 **Node.js** | **Entscheidend.** Entschlüsselt die Anti-Bot-Schutzmechanismen von YouTube, um mit maximaler Geschwindigkeit herunterzuladen. *(Muss in seinem Standardordner installiert sein: `C:\Program Files\nodejs`)*.<br>🔗 **[Node.js (LTS-Version) herunterladen](https://nodejs.org/)** |
| 🎬 **FFmpeg** | **Unverzichtbar.** Ein hochmodernes Tool, das 4K-Videostreams mit Ihrem gewählten Audio zusammenführt. *(Die ausführbare Datei muss zum Windows `PATH` hinzugefügt werden)*.<br>🔗 **[FFmpeg herunterladen (Windows-Builds)](https://www.gyan.dev/ffmpeg/builds/)** oder über [GitHub](https://github.com/BtbN/FFmpeg-Builds/releases) |
| 🌐 **Browser** | Ein Chromium-basierter Browser (Google Chrome, Microsoft Edge, Brave usw.). |

---

## ⚙️ Installationsanleitung

### 1️⃣ Den lokalen Server einrichten (Backend)
Der Server erledigt die schwere Arbeit im Hintergrund (Extrahieren und Zusammenführen).

1. Öffnen Sie ein Terminal (Eingabeaufforderung oder PowerShell) im Ordner `youtube-api`.
2. Installieren Sie die erforderlichen Python-Abhängigkeiten, indem Sie Folgendes eingeben:
   ```cmd
   pip install fastapi uvicorn yt-dlp
   ```
3. Starten Sie den Server:
   ```cmd
   python -m uvicorn main:app --reload
   ```
   > 💡 **Tipp:** Lassen Sie dieses Terminal offen. Der Server sucht bei jedem Start automatisch im Hintergrund nach Updates für `yt-dlp` (den Kern des Downloaders)!

### 2️⃣ Die Erweiterung installieren (Frontend)
1. Öffnen Sie Ihren Browser und gehen Sie zur Seite für die Erweiterungsverwaltung (geben Sie `chrome://extensions/` oder `edge://extensions/` in die Adressleiste ein).
2. Aktivieren Sie den **"Entwicklermodus"** (meist ein Schalter oben rechts).
3. Klicken Sie auf die Schaltfläche **"Entpackte Erweiterung laden"** (Load unpacked).
4. Wählen Sie den Stammordner der Erweiterung (den Hauptordner, der die Datei `manifest.json` enthält).

---

## 🚀 Tägliche Nutzung

1. **Vorbereitung**: Stellen Sie sicher, dass Ihr Python-Server (`main.py`) läuft.
2. **Navigation**: Gehen Sie zur gewünschten YouTube-Videoseite.
3. **Auswahl**: Klicken Sie auf das YouTuDo-Erweiterungssymbol in Ihrer Symbolleiste. Die Benutzeroberfläche öffnet sich und lädt alle verfügbaren Formate (einschließlich versteckter Audio-Synchronisationen).
4. **Download**: Wählen Sie die gewünschte Auflösung oder Audiospur und starten Sie den Download mit einem einzigen Klick!

> ⚠️ **Wichtiger Hinweis:** Schließen Sie Ihr Terminalfenster nicht, während ein Video heruntergeladen wird, da der Vorgang sonst abgebrochen wird.
