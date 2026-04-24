import yt_dlp
import traceback

def test_info():
    ydl_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': False}
    url = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Extracting info...")
            info = ydl.extract_info(url, download=False)
            print("Keys in info:", list(info.keys()))
            formats = info.get('formats', [])
            print(f"Got {len(formats)} formats.")
            if len(formats) > 0:
                print("First format keys:", list(formats[0].keys()))
    except Exception as e:
        print("ERROR INFO:", traceback.format_exc())

def test_download():
    ydl_opts = {
        'format': '18', # typically 360p mp4
        'outtmpl': 'downloads/%(id)s_%(format_id)s.%(ext)s',
        'quiet': False
    }
    url = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Downloading info...")
            info = ydl.extract_info(url, download=True)
            print("Filename prepare:")
            filename = ydl.prepare_filename(info)
            print("Prepared filename:", filename)
            
            # Let's check requested downloads
            reqs = info.get('requested_downloads', [])
            if reqs:
                print("Actual downloaded filepath:", reqs[0].get('filepath'))
    except Exception as e:
        print("ERROR DL:", traceback.format_exc())

print("--- TEST INFO ---")
test_info()
print("--- TEST DOWNLOAD ---")
test_download()
