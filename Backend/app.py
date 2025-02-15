from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Home route to check if the server is running
@app.route('/')
def home():
    return jsonify({"message": "Flask server is running!"})

# Test endpoint to verify API communication
@app.route('/test', methods=['POST'])
def test_api():
    # Get JSON data from the request
    data = request.get_json()

    # Check if "text" key is present in the received JSON
    if not data or "text" not in data:
        return jsonify({"error": "Invalid request, 'text' key is required"}), 400

    # Send back the received text as confirmation
    return jsonify({"received_text": data["text"]})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)