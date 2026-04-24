import yt_dlp

URL = 'https://www.youtube.com/watch?v=0e3GPea1Tyg' 
# Test avec différents clients pour voir les pistes audio
ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    # Forcer l'exploration des clients pour trouver les dowlads
    'extractor_args': {'youtube': {'player_client': ['android', 'web', 'ios']}}
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        formats = info.get('formats', [])
        
        print(f"{'ID':<6} {'EXT':<6} {'ABR':<6} {'LANG':<10} {'NOTE':<20}")
        print("-" * 60)
        for f in formats:
            if f.get('vcodec') == 'none': # Audio only
                lang = f.get('language') or f.get('language_preference')
                note = f.get('format_note') or ''
                # Si c'est une piste audio doublée, la note contient souvent le nom de la langue
                print(f"{f.get('format_id'):<6} {f.get('ext'):<6} {f.get('abr'):<6} {str(lang):<10} {str(note):<20}")
except Exception as e:
    print(f"Error: {e}")
