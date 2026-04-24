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
  <p><strong>L'Extension Premium de Téléchargement YouTube</strong></p>
</div>

---

**YouTuDo** est une extension de navigateur couplée à un serveur local puissant. Elle permet d'extraire et de télécharger des vidéos YouTube (y compris en **4K**) avec n'importe quelle piste audio, tout en contournant intelligemment les sécurités et le bridage de vitesse.

## ⚠️ Prérequis Système (PC)

Pour fonctionner de manière optimale, YouTuDo a besoin d'un petit "moteur" local. Assurez-vous d'avoir installé les éléments suivants :

| Logiciel | Description & Lien de téléchargement |
| :--- | :--- |
| 🐍 **Python 3** | Requis pour faire tourner le serveur API local.<br>🔗 **[Télécharger Python](https://www.python.org/downloads/windows/)** |
| 🟩 **Node.js** | **Crucial.** Permet de déchiffrer les sécurités anti-bot de YouTube pour télécharger à vitesse maximale. *(Il doit être installé dans son dossier par défaut : `C:\Program Files\nodejs`)*.<br>🔗 **[Télécharger Node.js (Version LTS)](https://nodejs.org/)** |
| 🎬 **FFmpeg** | **Indispensable.** Outil de pointe qui permet de fusionner les flux d'image 4K avec le son de votre choix. *(L'exécutable doit être ajouté au `PATH` de Windows)*.<br>🔗 **[Télécharger FFmpeg (Builds Windows)](https://www.gyan.dev/ffmpeg/builds/)** ou via [GitHub](https://github.com/BtbN/FFmpeg-Builds/releases) |
| 🌐 **Navigateur** | Un navigateur basé sur Chromium (Google Chrome, Microsoft Edge, Brave, etc.). |

---

## ⚙️ Guide d'Installation

### 1️⃣ Configurer le Serveur Local (Backend)
Le serveur est responsable de faire le travail lourd en arrière-plan (extraction et fusion).

1. Ouvrez un terminal (Invite de commandes ou PowerShell) dans le dossier `youtube-api`.
2. Installez les dépendances Python nécessaires en tapant :
   ```cmd
   pip install fastapi uvicorn yt-dlp
   ```
3. Lancez le serveur :
   ```cmd
   python -m uvicorn main:app --reload
   ```
   > 💡 **Astuce :** Laissez ce terminal ouvert. Le serveur vérifiera automatiquement s'il existe une mise à jour pour `yt-dlp` (le cœur du téléchargeur) en arrière-plan à chaque démarrage !

### 2️⃣ Installer l'Extension (Frontend)
1. Ouvrez votre navigateur et accédez à la page de gestion des extensions (tapez `chrome://extensions/` ou `edge://extensions/` dans la barre d'adresse).
2. Activez le **"Mode Développeur"** (généralement un interrupteur en haut à droite).
3. Cliquez sur le bouton **"Charger l'extension non empaquetée"** (Load unpacked).
4. Sélectionnez le dossier racine de l'extension (le dossier principal qui contient le fichier `manifest.json`).

---

## 🚀 Utilisation au Quotidien

1. **Préparation** : Assurez-vous que votre serveur Python (`main.py`) est bien en cours d'exécution.
2. **Navigation** : Allez sur la page de la vidéo YouTube de votre choix.
3. **Sélection** : Cliquez sur l'icône de l'extension YouTuDo dans votre barre d'outils. L'interface s'ouvrira et chargera tous les formats disponibles (y compris les doublages audio cachés).
4. **Téléchargement** : Choisissez la résolution ou la piste audio qui vous plaît et lancez le téléchargement d'un simple clic !

> ⚠️ **Note Importante :** Ne fermez pas la fenêtre de votre terminal pendant qu'une vidéo est en cours de téléchargement, sinon l'opération sera annulée.
