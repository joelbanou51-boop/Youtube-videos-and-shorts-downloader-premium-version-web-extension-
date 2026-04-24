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
  <p><strong>La Extensión Premium de Descarga de YouTube</strong></p>
</div>

---

**YouTuDo** es una extensión de navegador combinada con un potente servidor local. Te permite extraer y descargar vídeos de YouTube (incluyendo en **4K**) con cualquier pista de audio, evadiendo de manera inteligente las protecciones y las limitaciones de velocidad.

## ⚠️ Requisitos del Sistema (PC)

Para funcionar de manera óptima, YouTuDo necesita un pequeño "motor" local. Asegúrate de tener instalado lo siguiente:

| Software | Descripción y Enlace de Descarga |
| :--- | :--- |
| 🐍 **Python 3** | Requerido para ejecutar el servidor API local.<br>🔗 **[Descargar Python](https://www.python.org/downloads/windows/)** |
| 🟩 **Node.js** | **Crucial.** Permite descifrar las protecciones anti-bots de YouTube para descargar a máxima velocidad. *(Debe estar instalado en su carpeta por defecto: `C:\Program Files\nodejs`)*.<br>🔗 **[Descargar Node.js (Versión LTS)](https://nodejs.org/)** |
| 🎬 **FFmpeg** | **Indispensable.** Herramienta de vanguardia que fusiona el flujo de vídeo 4K con el audio de tu elección. *(El ejecutable debe ser agregado al `PATH` de Windows)*.<br>🔗 **[Descargar FFmpeg (Builds de Windows)](https://www.gyan.dev/ffmpeg/builds/)** o vía [GitHub](https://github.com/BtbN/FFmpeg-Builds/releases) |
| 🌐 **Navegador** | Un navegador basado en Chromium (Google Chrome, Microsoft Edge, Brave, etc.). |

---

## ⚙️ Guía de Instalación

### 1️⃣ Configurar el Servidor Local (Backend)
El servidor se encarga del trabajo pesado en segundo plano (extracción y fusión).

1. Abre una terminal (Símbolo del sistema o PowerShell) en la carpeta `youtube-api`.
2. Instala las dependencias necesarias de Python escribiendo:
   ```cmd
   pip install fastapi uvicorn yt-dlp
   ```
3. Inicia el servidor:
   ```cmd
   python -m uvicorn main:app --reload
   ```
   > 💡 **Consejo:** Mantén esta terminal abierta. ¡El servidor verificará automáticamente si hay actualizaciones para `yt-dlp` (el núcleo del descargador) en segundo plano cada vez que inicie!

### 2️⃣ Instalar la Extensión (Frontend)
1. Abre tu navegador y ve a la página de administración de extensiones (escribe `chrome://extensions/` o `edge://extensions/` en la barra de direcciones).
2. Activa el **"Modo de desarrollador"** (generalmente un interruptor en la esquina superior derecha).
3. Haz clic en el botón **"Cargar extensión sin empaquetar"** (Load unpacked).
4. Selecciona la carpeta raíz de la extensión (la carpeta principal que contiene el archivo `manifest.json`).

---

## 🚀 Uso Diario

1. **Preparación**: Asegúrate de que tu servidor Python (`main.py`) se esté ejecutando.
2. **Navegación**: Ve a la página del vídeo de YouTube que desees.
3. **Selección**: Haz clic en el icono de la extensión YouTuDo en tu barra de herramientas. La interfaz se abrirá y cargará todos los formatos disponibles (incluyendo pistas de audio ocultas).
4. **Descarga**: ¡Elige la resolución o la pista de audio que prefieras y comienza la descarga con un solo clic!

> ⚠️ **Nota Importante:** No cierres la ventana de tu terminal mientras un vídeo se está descargando, de lo contrario la operación se cancelará.
