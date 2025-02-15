import requests

url = "http://127.0.0.1:5000/test"
data = {"text": "Hello"}
response = requests.post(url, json=data)
print(response.json())