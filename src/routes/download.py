from flask import Blueprint, request, jsonify, send_file, send_from_directory
import os
import urllib.parse

if (os.getenv("FLASK_ENV") == "development"):
    from services.downloader import download_audio_from_playlist
else:
    from src.services.downloader import download_audio_from_playlist

download_bp = Blueprint('download', __name__)
DOWNLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
DELETE_AFTER_DOWNLOAD = True

@download_bp.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    direct_download = data.get('direct_download', False)

    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        print(f"Received URL: {url}")
        filename = download_audio_from_playlist(url)

        if not filename:
            return jsonify({'status': 'error', 'message': 'Download failed'}), 500

        file_path = os.path.join(DOWNLOADS_DIR, filename)

        if not os.path.isfile(file_path):
            return jsonify({'status': 'error', 'message': 'File not found'}), 404

        if direct_download:
            response = send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype='audio/mpeg'
            )

            if DELETE_AFTER_DOWNLOAD:
                @response.call_on_close
                def cleanup():
                    try:
                        os.remove(file_path)
                        print(f"[INFO] Deleted after download: {file_path}")
                    except Exception as e:
                        print(f"[ERROR] Cleanup failed: {e}")

            return response
        else:
            return jsonify({
                'status': 'success',
                'message': 'Download complete',
                'filename': filename,
                'download_url': f'/download/{filename}'
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

