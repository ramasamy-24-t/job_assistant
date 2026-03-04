import requests
import json

# 1. Login to get token
login_data = {"email": "test@example.com", "password": "password"} # Make sure this user exists or create them
response = requests.post("http://127.0.0.1:5000/api/auth/login", json=login_data)

if response.status_code != 200:
    # Attempt signup
    response = requests.post("http://127.0.0.1:5000/api/auth/signup", json={"name": "test", "email": "test@example.com", "password": "password"})
    response = requests.post("http://127.0.0.1:5000/api/auth/login", json=login_data)

token = response.json().get('access_token')

if not token:
    print("Failed to get token!")
    exit(1)

# 2. Upload file
print(f"Token: {token}")

files = {'file': ('test.pdf', b'%PDF-1.4 test file mock', 'application/pdf')}
headers = {'Authorization': f'Bearer {token}'}

resp = requests.post("http://127.0.0.1:5000/api/resume/upload", files=files, headers=headers)
print(f"Status Code: {resp.status_code}")
print(f"Response: {resp.text}")
