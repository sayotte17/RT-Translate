import deepl, whisper, os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import whisper

model = whisper.load_model("tiny")

DEEPL_API_KEY = "b72f940b-e07b-4985-b78c-16cd67c7af51:fx"
translator = deepl.Translator(DEEPL_API_KEY)

@app.route('/translate', methods=['POST'])
def translate_text():
    if request.method == 'OPTIONS':
        return jsonify({"message": "CORS preflight OK"}), 200
    try:
        data = request.json
        if 'text' not in data or 'target_lang' not in data:
            return jsonify({"error": "Missing 'text' or 'target_lang' in request"}), 400

        text = data['text']
        target_lang = data['target_lang'].upper()  # DeepL uses uppercase language codes

        translation = translator.translate_text(text, target_lang=target_lang)

        return jsonify({"translated_text": translation.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    try:
        # Check if an audio file is in the request
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        audio_file = request.files['audio']

        # Save the file temporarily
        file_path = "temp_audio.wav"
        audio_file.save(file_path)

        # Transcribe the audio
        result = model.transcribe(file_path)

        # Delete the temporary file
        os.remove(file_path)

        return jsonify({"transcribed_text": result["text"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)