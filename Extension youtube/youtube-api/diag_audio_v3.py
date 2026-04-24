import yt_dlp

URL = 'https://www.youtube.com/watch?v=0e3GPea1Tyg' 
ydl_opts = {
    'quiet': True,
    'extract_flat': False,
    'no_warnings': True,
    'youtube_include_dash_manifest': True,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        formats = info.get('formats', [])
        
        print(f"{'ID':<15} {'LANG':<10} {'EXT':<6} {'NOTE'}")
        print("-" * 60)
        for f in formats:
            # On cherche tout ce qui n'a pas de vidéo
            if f.get('vcodec') == 'none':
                lang = f.get('language')
                note = f.get('format_note')
                fid = f.get('format_id')
                ext = f.get('ext')
                print(f"{str(fid):<15} {str(lang):<10} {str(ext):<6} {str(note)}")
except Exception as e:
    print(f"Error: {e}")
