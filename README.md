# **YouTube Music API**

A Flask-based API that lets you download YouTube playlists or individual videos as audio files. It also allows you to fetch metadata (like playlist title, video titles, and URLs) using YouTube's Data API.

## ✨ **Features**
- Download a **single video** or an entire **playlist** as `.mp3`.
- Fetch and return **playlist metadata**, including titles and video links.
- Automatically converts audio to high-quality MP3 format.
- Optional cleanup of downloaded files after serving.
- **Configurable behavior**: Choose between a **single POST** request (with direct download) or a **POST + GET** flow to download the file.
- **Environment-based path imports**: Automatically adjusts import paths based on the environment (development or production).

---

## 🧰 **Installation**

### 1. Clone the repo
```bash
git clone https://github.com/wafardev/youtube-music-api.git
cd youtube-music-api
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your environment variables
Create a `.env` file in the project root:
```
API_KEY=your_youtube_data_api_key
FFMPEG_PATH=/absolute/path/to/ffmpeg
FLASK_ENV=development  # or production
```

---

## 🚀 **Running the app**

### Running Locally
To run the application in development mode, execute the following command:
```bash
python3 src/app.py
```

The server will be available at `http://127.0.0.1:5000`.

### Running with Gunicorn (for production)
If you're ready to run the app in production, use Gunicorn:
```bash
gunicorn src.app:app
```

---

## 📡 **API Endpoints**

### ▶️ **POST `/download`**

Downloads a YouTube video or playlist as MP3 on the server.

#### ✅ Request
```json
{
  "url": "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID",
  "direct_download": true
}
```
or
```json
{
  "url": "https://www.youtube.com/watch?v=SINGLE_VIDEO_ID"
}
```

- `direct_download`: Optional flag to specify if the download should be **directly returned** in the response. If `false` or omitted, the response will contain a URL for later downloading.

#### 🔁 Response (direct download)
```json
{
  "status": "success",
  "files": ["Track 1.mp3", "Track 2.mp3"]
}
```

#### 🔁 Response (POST + GET flow)
```json
{
  "status": "success",
  "message": "Download complete",
  "filename": "Track 1.mp3",
  "download_url": "/download/Track%201.mp3"
}
```

---

### 📥 **GET `/download/<filename>`**

Downloads a specific MP3 file by filename from the server.

#### ✅ Example
```bash
curl -O http://127.0.0.1:5000/download/Track%201.mp3
```

---

### 📋 **POST `/playlist`**

Fetch metadata (playlist ID, title, and list of videos) from a playlist URL.

#### ✅ Request
```json
{
  "playlist_url": "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
}
```

#### 🔁 Response
```json
{
  "playlist_id": "abc123",
  "playlist_title": "My Favorite Jams",
  "videos": [
    {"title": "Cool Song 1", "url": "https://youtube.com/watch?v=123"},
    {"title": "Cool Song 2", "url": "https://youtube.com/watch?v=456"}
  ]
}
```

---

## 🧪 **Testing with `curl`**

### Download a playlist (direct download):
```bash
curl -X POST http://127.0.0.1:5000/download \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/playlist?list=YOUR_ID", "direct_download": true}' \
     -OJ
```

### Download a playlist (POST + GET flow):
```bash
curl -X POST http://127.0.0.1:5000/download \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/playlist?list=YOUR_ID"}'
```
Then, download the file later:
```bash
curl -O http://127.0.0.1:5000/download/Track%201.mp3
```

---

## 📜 **License**
MIT — free to use and modify.

---

### 🚨 **How It Works:**

- The `/download` endpoint supports two behaviors:
  - **Direct download** via a single POST request (`direct_download: true`) — the file is immediately returned to the client.
  - **POST + GET** — the POST request responds with a metadata object that includes a `download_url`, which can later be used to download the file via a GET request.

You can choose the behavior with the `direct_download` flag in the POST request. If set to `true`, the file will be served directly in the POST response. If omitted or set to `false`, you will get a URL to download the file later.

### 🌍 **Environment-based Imports:**

- The app uses **environment variables** to adjust its behavior between development and production environments.
- In **development**, the imports are simpler (directly from the `routes` directory).
- In **production**, it adjusts to import from the `src.routes` directory, ensuring flexibility for different deployment environments.