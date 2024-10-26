from flask import request, jsonify, send_file
import yt_dlp
import os
import uuid

def register_routes(app):
    @app.route('/api/download', methods=['POST'])
    def download_video():
        data = request.json
        video_url = data.get('url')
        format = data.get('format', 'mp4')
        resolution = data.get('resolution', '720p')

        if not video_url:
            return jsonify({'error': 'URL do vídeo não fornecida'}), 400

        try:
            ydl_opts = {
                'format': f'bestvideo[height<={resolution[:-1]}]+bestaudio/best[height<={resolution[:-1]}]',
                'outtmpl': os.path.join(app.config['DOWNLOAD_FOLDER'], f'{uuid.uuid4()}.%(ext)s'),
            }

            if format == 'mp3':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                
                if format == 'mp3':
                    filename = os.path.splitext(filename)[0] + '.mp3'

            return jsonify({
                'success': True,
                'message': 'Vídeo baixado com sucesso',
                'filename': os.path.basename(filename)
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/download/<filename>', methods=['GET'])
    def serve_file(filename):
        return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_attachment=True)
