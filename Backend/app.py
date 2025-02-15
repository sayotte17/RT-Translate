import deepl
from flask import Flask, request, jsonify

app = Flask(__name__)

DEEPL_API_KEY = "b72f940b-e07b-4985-b78c-16cd67c7af51:fx"
translator = deepl.Translator(DEEPL_API_KEY)

@app.route('/translate', methods=['POST'])
def translate_text():
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)