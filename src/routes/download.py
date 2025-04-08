from flask import Blueprint, request, jsonify, send_from_directory
from services.downloader import download_audio_from_playlist
import urllib.parse
import os

download_bp = Blueprint('download', __name__)
DOWNLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
DELETE_AFTER_DOWNLOAD = True

@download_bp.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'Missing playlist URL'}), 400

    try:
        print(f"Received URL: {url}")
        filename = download_audio_from_playlist(url)

        if not filename:
            return jsonify({'status': 'error', 'message': 'Download failed'}), 500
        
        return jsonify({
            'status': 'success',
            'message': 'Download complete',
            'filename': filename,
            'download_url': f'/download/{urllib.parse.quote(filename)}'
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def is_safe_filename(filename):
    basename = os.path.basename(filename)
    return basename == filename

@download_bp.route('/download/<path:filename>', methods=['GET'])
def serve_file(filename):
    decoded_filename = urllib.parse.unquote(filename)

    if not is_safe_filename(decoded_filename):
        return jsonify({'error': 'Invalid filename'}), 400

    file_path = os.path.join(DOWNLOADS_DIR, decoded_filename)

    if not os.path.isfile(file_path):
        return jsonify({'error': 'File not found'}), 404

    response = send_from_directory(
        DOWNLOADS_DIR,
        decoded_filename,
        as_attachment=True,
        mimetype='audio/mpeg'
    )

    if DELETE_AFTER_DOWNLOAD:
        @response.call_on_close
        def cleanup():
            print(f"[INFO] Cleaning up: {file_path}")
            try:
                os.remove(file_path)
                print(f"[INFO] Deleted: {file_path}")
            except Exception as e:
                print(f"[ERROR] Failed to delete {file_path}: {e}")

    return response

