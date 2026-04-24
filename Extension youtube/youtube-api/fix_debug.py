import yt_dlp
import os
import sys

# MrBeast video for test
URL = 'https://www.youtube.com/watch?v=0e3GPea1Tyg'

ydl_opts = {
    'quiet': False, # See errors
    'no_warnings': False,
    'extractor_args': {'youtube': {'player_client': ['android', 'web', 'ios']}}
}

print(f"Testing with yt-dlp version: {yt_dlp.version.__version__}")

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        formats = info.get('formats', [])
        print(f"Successfully extracted {len(formats)} formats.")
        if len(formats) > 0:
            print(f"Example ID: {formats[0].get('format_id')} URL: {str(formats[0].get('url'))[:30]}...")
except Exception as e:
    print(f"Error during extraction: {e}")
