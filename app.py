from flask import Flask, jsonify, render_template, request
import requests, os, json

app = Flask(__name__, template_folder=os.path.join('Frontend', 'templates'))

def load_stats():
    """Load stats from db.json, or return defaults if not found."""
    if not os.path.exists('Backend/db.json'):
        # If file doesn't exist, return default stats
        return {"translations_processed": 0, "words_translated": 0}
    
    with open('Backend/db.json', 'r') as f:
        return json.load(f)

# Route for 'home.html'
@app.route('/')
def home():
    return render_template('home.html')

# Route for 'translator.html'
@app.route('/translator')
def translator():
    return render_template('translator.html')

# Route for 'about.html'
@app.route('/about')
def about():
    stats = load_stats()
    # Pass them to the template
    return render_template(
        'about.html',
        translations_processed=stats["translations_processed"],
        words_translated=stats["words_translated"]
    )
    

# Example API endpoint (JSON response)
@app.route('/api')
def chicken():
    return jsonify({"message": "quack"})

if __name__ == '__main__':
    # Adjust host and port as needed
    app.run(debug=True, host='0.0.0.0', port=3000)