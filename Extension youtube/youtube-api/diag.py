import yt_dlp
import sys

URL = 'https://www.youtube.com/watch?v=aqz-KE-bpKQ'
ydl = yt_dlp.YoutubeDL({'quiet': True})
info = ydl.extract_info(URL, download=False)
formats = info.get('formats', [])

print(f"{'ID':<10} {'Res':<10} {'Ext':<5} {'V-Codec':<20} {'A-Codec':<20}")
print("-" * 70)
for f in formats:
    v = f.get('vcodec')
    a = f.get('acodec')
    h = f.get('height')
    fid = f.get('format_id')
    ext = f.get('ext')
    print(f"{fid:<10} {h if h else 'N/A':<10} {ext:<5} {str(v):<20} {str(a):<20}")
