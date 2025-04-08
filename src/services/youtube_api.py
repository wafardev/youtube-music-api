import requests
import os
import re

API_KEY = os.getenv('YOUTUBE_API_KEY')

if not API_KEY:
    raise EnvironmentError("YOUTUBE_API_KEY environment variable not set. Please set it to your YouTube API key.")

def extract_playlist_id(url):
    pattern = r"list=([a-zA-Z0-9_-]+)"
    
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    else:
        return False 

import requests

def fetch_playlist_videos(playlist_url):
    base_url_playlist = "https://www.googleapis.com/youtube/v3/playlists"
    base_url_items = "https://www.googleapis.com/youtube/v3/playlistItems"
    video_links = []
    video_titles = []
    next_page_token = None

    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        return {'error': 'Invalid playlist URL', 'details': 'Unable to extract playlist ID'}
    
    print(f"Extracted Playlist ID: {playlist_id}")

    try:
        playlist_params = {
            'part': 'snippet',
            'id': playlist_id,
            'key': API_KEY
        }

        playlist_response = requests.get(base_url_playlist, params=playlist_params)
        playlist_response.raise_for_status()
        playlist_data = playlist_response.json()

        if 'items' not in playlist_data or not playlist_data['items']:
            return {'error': 'Failed to fetch playlist info', 'details': playlist_data}

        playlist_title = playlist_data['items'][0]['snippet']['title']
        print(f"Playlist Title: {playlist_title}")
    except requests.exceptions.RequestException as e:
        return {'error': 'Request failed', 'details': str(e)}

    while True:
        params = {
            'part': 'snippet',
            'maxResults': 50,  # Number of items per page (maximum allowed by YouTube API)
            'playlistId': playlist_id,
            'key': API_KEY,
            'pageToken': next_page_token
        }

        try:
            response = requests.get(base_url_items, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {'error': 'Request failed', 'details': str(e)}

        data = response.json()

        if 'items' not in data:
            return {'error': 'Failed to fetch playlist info', 'details': data}

        for item in data['items']:
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            video_links.append(f"https://www.youtube.com/watch?v={video_id}")
            video_titles.append(title)

        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return {
        'playlist_id': playlist_id,
        'playlist_title': playlist_title,
        'videos': [{'title': title, 'url': link} for title, link in zip(video_titles, video_links)]
    }
