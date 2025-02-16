import deepl, whisper, os, json, ssl, urllib.request
from flask import Flask, request, jsonify
from flask_cors import CORS

# Disable SSL verification globally
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
CORS(app)

model = whisper.load_model("turbo")

DEEPL_API_KEY = "b72f940b-e07b-4985-b78c-16cd67c7af51:fx"
translator = deepl.Translator(DEEPL_API_KEY)

def load_stats():
    """Load stats from db.json, or return defaults if not found."""
    if not os.path.exists('db.json'):
        # If file doesn't exist, return default stats
        return {"translations_processed": 0, "words_translated": 0}
    
    with open('db.json', 'r') as f:
        return json.load(f)

def save_stats(stats):
    """Save stats dictionary to db.json."""
    with open('db.json', 'w') as f:
        json.dump(stats, f)

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

        # --- NEW CODE: update stats ---
        stats = load_stats()
        stats["translations_processed"] += 1
        stats["words_translated"] += len(text.split())
        save_stats(stats)
        # --- END NEW CODE ---

        return jsonify({"translated_text": translation.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/speech_to_text', methods=['POST'])
def speech_to_text_and_translate():
    """
    Expects:
      - `audio`: The uploaded audio file (e.g., WAV, MP3, etc.)
      - `target_lang`: The language code to translate into
    Returns:
      - JSON with the 'transcribed_text' and 'translated_text'
    """
    try:
        # Check for the audio file
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        # Get target language (e.g., from form data or JSON body)
        target_lang = request.form.get('target_lang') or request.args.get('target_lang')
        if not target_lang and request.is_json:
            data = request.get_json()
            target_lang = data.get('target_lang')

        if not target_lang:
            return jsonify({"error": "No target language provided"}), 400

        # Save the file temporarily
        audio_file = request.files['audio']
        file_path = "temp_audio.wav"
        audio_file.save(file_path)

        # 1) Transcribe the audio with Whisper
        result = model.transcribe(file_path)
        transcribed_text = result["text"]

        # 2) Translate the transcribed text with DeepL
        target_lang = target_lang.upper()  # DeepL requires uppercase
        translation = translator.translate_text(transcribed_text, target_lang=target_lang)
        translated_text = translation.text

        # Clean up
        os.remove(file_path)

        # --- NEW CODE: update stats ---
        stats = load_stats()
        # You might want to track "speech translations processed" and "spoken words" differently.
        stats["translations_processed"] += 1
        stats["words_translated"] += len(transcribed_text.split())
        save_stats(stats)
        # --- END NEW CODE ---


        # Return both raw transcription and final translation
        return jsonify({
            "transcribed_text": transcribed_text,
            "translated_text": translated_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)