import yt_dlp
import sys

# MrBeast video (often has many dubs)
URL = 'https://www.youtube.com/watch?v=0e3GPea1Tyg' 
ydl_opts = {'quiet': True, 'no_warnings': True}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        formats = info.get('formats', [])
        
        print(f"{'ID':<6} {'EXT':<6} {'ABR':<6} {'LANG':<10} {'NOTE':<20}")
        print("-" * 60)
        for f in formats:
            if f.get('vcodec') == 'none': # Audio only
                print(f"{f.get('format_id'):<6} {f.get('ext'):<6} {f.get('abr'):<6} {str(f.get('language')):<10} {str(f.get('format_note')):<20}")
except Exception as e:
    print(f"Error: {e}")
