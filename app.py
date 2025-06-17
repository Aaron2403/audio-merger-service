from flask import Flask, request, jsonify, send_file
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Servicio de unión de audio está activo."

@app.route('/merge_audio', methods=['POST'])
def merge_audio():
    temp_dir = '/tmp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    if 'file' not in request.files:
        return jsonify({"error": "No se recibieron archivos"}), 400

    files = request.files.getlist('file')
    saved_files = []

    for f in files:
        file_path = os.path.join(temp_dir, f.filename)
        f.save(file_path)
        saved_files.append(file_path)
    
    saved_files.sort()

    combined_audio = AudioSegment.empty()
    for file_path in saved_files:
        try:
            segment = AudioSegment.from_mp3(file_path)
            combined_audio += segment
        except Exception as e:
            return jsonify({"error": f"Error procesando {file_path}: {str(e)}"}), 500
    
    final_audio_path = os.path.join(temp_dir, 'final_voiceover.mp3')
    combined_audio.export(final_audio_path, format="mp3")

    return send_file(final_audio_path, as_attachment=True)