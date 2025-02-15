from flask import Flask, jsonify, render_template

import os
app = Flask(__name__, template_folder=os.path.join('Frontend', 'templates'))



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api')
def chicken():
    return jsonify({"message": "quack"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
