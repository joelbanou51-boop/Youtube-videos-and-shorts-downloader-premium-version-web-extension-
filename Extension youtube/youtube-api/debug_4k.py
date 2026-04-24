import yt_dlp
import os

# Ensure Node is in PATH for this test too
node_path = r"C:\Program Files\nodejs"
if os.path.exists(node_path) and node_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + node_path

URL = 'https://www.youtube.com/watch?v=aqz-KE-bpKQ'
ydl_opts = {'quiet': True, 'no_warnings': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)
    formats = info.get('formats', [])
    
    print(f"{'ID':<6} {'Res':<6} {'HasURL':<8} {'V-Codec':<15} {'A-Codec':<15}")
    for f in formats:
        h = f.get('height')
        if h and h >= 1440:
            print(f"{f.get('format_id'):<6} {h:<6} {str(f.get('url') is not None):<8} {str(f.get('vcodec')):<15} {str(f.get('acodec')):<15}")
