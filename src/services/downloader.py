import os
import yt_dlp as ytdl

FFMPEG_PATH = os.getenv('FFMPEG_PATH')

if not FFMPEG_PATH:
    raise EnvironmentError("FFMPEG_PATH environment variable not set. Please set it to the path of ffmpeg executable.")

DOWNLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')

if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

def download_audio_from_playlist(url):
    ydl_opts = {
        'ffmpeg_location': FFMPEG_PATH,
        'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best', 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3', 
            'preferredquality': '192',
        }],
    }

    print(f"Downloading audio from {url}...")

    try:
        with ytdl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            
            filename = ydl.prepare_filename(info_dict)
            filename = filename.replace('.webm', '.mp3')
            filename = os.path.basename(filename)

        print(f"Download completed successfully: {filename}")
        return filename 
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None