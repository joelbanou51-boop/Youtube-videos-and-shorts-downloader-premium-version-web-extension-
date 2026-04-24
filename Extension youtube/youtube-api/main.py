from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp
import os
import uuid
import threading
import time
import sys
import subprocess
import re

# --- AUTO-UPDATE YT-DLP (En arrière-plan) ---
def auto_update_yt_dlp():
    try:
        # On attend 2 sec pour laisser le serveur démarrer
        time.sleep(2)
        print("Vérification des mises à jour de yt-dlp en tâche de fond...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"], check=True, capture_output=True)
        print("yt-dlp est à jour.")
    except Exception as e:
        print(f"Échec de la mise à jour automatique : {e}")

# Lancement dans un thread séparé pour ne pas bloquer le démarrage
threading.Thread(target=auto_update_yt_dlp, daemon=True).start()

# Ajout manuel de Node.js au PATH (indispensable pour les signatures YouTube / 4K)
node_path = r"C:\Program Files\nodejs"
if os.path.exists(node_path) and node_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + node_path

app = FastAPI(title="YouTuDo Job API")

# Configuration
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Nettoyage au démarrage : on vide le dossier downloads pour repartir de zéro
def startup_clean():
    try:
        import shutil
        for filename in os.listdir(DOWNLOAD_DIR):
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Erreur lors du nettoyage au démarrage ({file_path}): {e}")
        print("Dossier 'downloads' nettoyé au démarrage.")
    except Exception as e:
        print(f"Échec du nettoyage initial : {e}")

startup_clean()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DownloadCancelled(Exception): pass

# Gestion des Jobs
jobs = {}

class DownloadJob:
    def __init__(self, task_id, url, format_id, merge_id=None):
        self.task_id, self.url, self.format_id, self.merge_id = task_id, url, format_id, merge_id
        self.status = "waiting" # downloading, merging, finished, error, cancelled
        self.progress, self.speed, self.eta = 0, "0 KB/s", ""
        self.filename, self.error = None, None
        self.stop_requested = False

    def progress_hook(self, d):
        if self.stop_requested: raise DownloadCancelled()
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try: self.progress = float(p)
            except: pass
            self.speed, self.eta, self.status = d.get('_speed_str', 'N/A'), d.get('_eta_str', ''), "downloading"
        elif d['status'] == 'finished':
            self.status, self.progress = "merging", 100

def run_download(job: DownloadJob):
    dl_fmt = f"{job.format_id}+{job.merge_id}" if job.merge_id else job.format_id
    ydl_opts = {
        'format': dl_fmt,
        'outtmpl': f'{DOWNLOAD_DIR}/{job.task_id}_%(title)s.%(ext)s',
        'merge_output_format': 'mp4' if job.merge_id else None,
        'progress_hooks': [job.progress_hook],
        'quiet': True, 'no_warnings': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            i = ydl.extract_info(job.url, download=True)
            # On cherche le fichier final produit dans le dossier downloads
            # yt-dlp peut changer l'extension après fusion, donc on scanne le dossier
            for f in os.listdir(DOWNLOAD_DIR):
                if f.startswith(job.task_id):
                    job.filename = os.path.join(DOWNLOAD_DIR, f)
                    break
            
            if not job.filename or not os.path.exists(job.filename):
                # Fallback si le scan échoue
                job.filename = ydl.prepare_filename(i)
                if job.merge_id and not job.filename.endswith('.mp4'):
                    job.filename = os.path.splitext(job.filename)[0] + '.mp4'
            
            job.status = "finished"
    except DownloadCancelled: job.status = "cancelled"
    except Exception as e: job.status, job.error = "error", str(e)
    finally:
        # Si le job s'arrête sans être "finished", on essaie de supprimer le fichier partiel s'il existe
        if job.status != "finished" and job.filename and os.path.exists(job.filename):
            try: os.remove(job.filename)
            except: pass

def map_format(f):
    v_codec = f.get('vcodec')
    a_codec = f.get('acodec')
    has_v = v_codec is not None and v_codec != 'none'
    has_a = a_codec is not None and a_codec != 'none'

    if has_v and has_a: f_t = "muxed"
    elif has_v: f_t = "video-only"
    else: f_t = "audio-only"
    ql = f.get('format_note') or f.get('resolution') or (f"{f.get('height')}p" if f.get('height') else None)
    lang_info = f.get('language') or f.get('language_preference') or 'und'
    # On essaie d'extraire un label plus lisible pour la langue si dispo (ex: format_note contient souvent le nom complet)
    note = f.get('format_note') or ''
    lang_label = lang_info
    if 'dubbed' in note.lower() or 'original' in note.lower():
        # Extraction du premier mot avant la parenthèse ou virgule pour isoler le nom de la langue
        lang_label = note.split('(')[0].split(',')[0].strip()

    return {
        "itag": f.get('format_id'), "type": f_t, "qualityLabel": ql, 
        "container": f.get('ext','').upper(), "ext": f.get('ext',''),
        "filesize": f.get('filesize') or f.get('filesize_approx') or 0,
        "url": f.get('url'), "height": f.get('height'),
        "language": lang_info,
        "languageName": lang_label,
        "abr": f.get('abr')
    }

@app.get("/api/info")
async def get_info(url: str):
    # On définit une fonction synchrone pour l'extraction afin de l'exécuter dans un pool de threads
    def extract():
        ydl_opts = {
            'quiet':True, 
            'no_warnings':True,
            'socket_timeout': 10, # Évite de bloquer trop longtemps
            'retries': 2,
            'nocheckcertificate': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    try:
        # On utilise Starlette's run_in_threadpool pour ne pas bloquer l'event loop asyncio
        from starlette.concurrency import run_in_threadpool
        i = await run_in_threadpool(extract)
        raw_formats = i.get('formats', [])
        
        # 1. Map des formats
        mapped = [map_format(f) for f in raw_formats if f.get('url')]
        
        # 2. Tri par qualité (décroissant)
        # - Vidéo : par hauteur
        # - Audio : par bitrate (abr)
        mapped.sort(key=lambda x: (x.get('height') or 0, x.get('abr') or 0), reverse=True)
        
        # 3. Dédoublonnage intelligent
        seen = set()
        unique_formats = []
        for f in mapped:
            if f['type'] == 'audio-only':
                # Pour l'audio : un seul par (langue + extension) -> le meilleur sortira en premier grâce au tri
                key = (f['type'], f['language'], f['ext'])
            else:
                # Pour la vidéo : un seul par (résolution + extension)
                key = (f['type'], f['height'], f['ext'])
            
            if key not in seen:
                unique_formats.append(f)
                seen.add(key)
        
        return {
            "success":True, 
            "videoTitle":i.get('title'), 
            "channelName":i.get('uploader'), 
            "thumbnail":i.get('thumbnail'), 
            "duration":i.get('duration'), 
            "formats":unique_formats
        }
    except Exception as e:
        print(f"Erreur extraction: {e}")
        return {"success":False, "error":str(e)}

@app.get("/api/health")
async def health():
    return {"status": "ok", "time": time.time()}

@app.post("/api/download/start")
async def start_dl(request: Request):
    data = await request.json()
    task_id = str(uuid.uuid4())[:8]
    job = DownloadJob(task_id, data['url'], data['format_id'], data.get('merge_id'))
    jobs[task_id] = job
    threading.Thread(target=run_download, args=(job,)).start()
    return {"success": True, "task_id": task_id}

@app.get("/api/download/status/{task_id}")
async def get_status(task_id: str):
    j = jobs.get(task_id)
    if not j: raise HTTPException(404)
    clean_name = os.path.basename(j.filename) if j.filename else None
    if clean_name:
        if clean_name.startswith(f"{j.task_id}_"):
            clean_name = clean_name[len(j.task_id)+1:]
        clean_name = re.sub(r'\s*\[.*?\](?=\.[^.]+$)', '', clean_name)
    return {"status":j.status, "progress":j.progress, "speed":j.speed, "filename":clean_name, "error":j.error}

@app.post("/api/download/cancel/{task_id}")
async def cancel_dl(task_id: str):
    j = jobs.get(task_id)
    if j: j.stop_requested = True
    return {"success": True}

@app.get("/api/download/file/{task_id}")
async def get_file(task_id: str, bt: BackgroundTasks):
    j = jobs.get(task_id)
    if not j or j.status != "finished" or not os.path.exists(j.filename): raise HTTPException(400)
    bt.add_task(lambda p: os.remove(p) if os.path.exists(p) else None, j.filename)
    # On retire l'identifiant technique (task_id_) pour que l'utilisateur ait un nom propre
    clean_name = os.path.basename(j.filename)
    if clean_name.startswith(f"{j.task_id}_"):
        clean_name = clean_name[len(j.task_id)+1:]
    
    # On retire aussi tout identifiant final technique ajouté par yt-dlp (ex: [format_id] ou [video_id])
    clean_name = re.sub(r'\s*\[.*?\](?=\.[^.]+$)', '', clean_name)
    
    return FileResponse(j.filename, filename=clean_name)
