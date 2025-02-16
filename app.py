from flask import Flask, jsonify, render_template, request
import requests
import os

app = Flask(__name__, template_folder=os.path.join('Frontend', 'templates'))

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
    return render_template('about.html')

# Example API endpoint (JSON response)
@app.route('/api')
def chicken():
    return jsonify({"message": "quack"})

if __name__ == '__main__':
    # Adjust host and port as needed
    app.run(debug=True, host='0.0.0.0', port=3000)