# **YouTube Music API**

A Flask-based API that lets you download YouTube playlists or individual videos as audio files. It also allows you to fetch metadata (like playlist title, video titles, and URLs) using YouTube's Data API.

## ✨ **Features**
- Download a **single video** or an entire **playlist** as `.mp3`.
- Fetch and return **playlist metadata**, including titles and video links.
- Automatically converts audio to high-quality MP3 format.
- Optional cleanup of downloaded files after serving.

---

## 🧰 **Installation**

### 1. Clone the repo
```bash
git clone https://github.com/wafardev/youtube-music-api.git
cd youtube-music-api
```

### 2. Create virtual environment
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
```

---

## 🚀 **Running the app**

```bash
python3 src/app.py
```

The server will be available at `http://127.0.0.1:5000`.

---

## 📡 **API Endpoints**

### ▶️ **POST `/download`**

Downloads a YouTube video or playlist as MP3 on the server.

#### ✅ Request
```json
{
  "url": "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
}
```
or
```json
{
  "url": "https://www.youtube.com/watch?v=SINGLE_VIDEO_ID"
}
```

#### 🔁 Response
```json
{
  "status": "success",
  "files": ["Track 1.mp3", "Track 2.mp3"]
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

Download a playlist:
```bash
curl -X POST http://127.0.0.1:5000/download \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/playlist?list=YOUR_ID"}'
```

Download a file:
```bash
curl -O http://127.0.0.1:5000/download/Track%201.mp3
```

---

## 📜 **License**
MIT — free to use and modify.

---