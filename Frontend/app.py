from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def chicken():
    return jsonify ({"message": "quack"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)