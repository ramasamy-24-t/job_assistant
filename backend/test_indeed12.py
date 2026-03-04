import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

rapid_api_key = os.environ.get('RAPID_API')
headers = {
    "x-rapidapi-key": rapid_api_key,
    "x-rapidapi-host": "indeed12.p.rapidapi.com"
}

url = "https://indeed12.p.rapidapi.com/jobs/search"
params = {"query": "Microbiologist", "location": "Coimbatore", "locality": "in"}
print(f"Testing {url} with {params}...")

try:
    response = requests.get(url, headers=headers, params=params)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Found hits: {len(data.get('hits', []))}")
        with open('cached_indeed_microbiologist_in.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        if data.get('hits'):
            first_job = data['hits'][0]
            print(f"First Job: {first_job.get('title')} at {first_job.get('company_name')} - {first_job.get('location')}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")
