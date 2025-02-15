import requests

url = "http://localhost:5000/test"
data = {"text": "Hello"}
response = requests.post(url, json=data)
print(response.json())
