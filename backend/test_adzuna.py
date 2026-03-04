import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

app_id = os.environ.get('ADZUNA_APP_ID')
app_key = os.environ.get('ADZUNA_APP_KEY')

url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
params = {
    "app_id": app_id,
    "app_key": app_key,
    "results_per_page": 20,
    "what": "Developer",
    "where": "Coimbatore"
}

print(f"Testing Adzuna API...")
try:
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        print(f"Success! Found {len(results)} jobs.")
        if results:
            first_job = results[0]
            print(f"First Job: {first_job.get('title')} at {first_job.get('company', {}).get('display_name')} - {first_job.get('location', {}).get('display_name')}")
            with open('cached_adzuna.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")
