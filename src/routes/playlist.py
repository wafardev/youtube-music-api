from flask import Blueprint, request, jsonify
from services.youtube_api import fetch_playlist_videos
import os

API_KEY = os.getenv('YOUTUBE_API_KEY')

if not API_KEY:
    print("YOUTUBE_API_KEY environment variable not set. Please set it to your YouTube API key.")
else:
    print("YOUTUBE_API_KEY is set.")
    
    playlist_bp = Blueprint('playlist', __name__)

    @playlist_bp.route('/playlist', methods=['POST'])
    def playlist():
        data = request.get_json()
        playlist_url = data.get('playlist_url')

        if not playlist_url:
            return jsonify({'error': 'Missing playlist ID'}), 400

        try:
            result = fetch_playlist_videos(playlist_url)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': 'Failed to fetch playlist', 'message': str(e)}), 500
