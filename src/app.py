from flask import Flask
from routes.download import download_bp
from routes.playlist import playlist_bp
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time

app = Flask(__name__)

app.register_blueprint(download_bp)
app.register_blueprint(playlist_bp)

DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), 'downloads')

scheduler = BackgroundScheduler()

def cleanup_old_files():
    now = time.time()
    for filename in os.listdir(DOWNLOADS_DIR):
        file_path = os.path.join(DOWNLOADS_DIR, filename)
        
        # Check if it's a file and if it is older than 10 minutes (600 seconds)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > 600:
                print(f"Deleting file: {filename} (Older than 10 minutes)")
                os.remove(file_path)

scheduler.add_job(func=cleanup_old_files, trigger="interval", minutes=10)

scheduler.start()

@app.route('/')
def index():
    return "Music Downloader and Player"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
