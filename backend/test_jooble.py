import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('JOOBLE_API_KEY')
url = f"https://jooble.org/api/{api_key}"
headers = {"Content-Type": "application/json"}

# Trial 1: Inject city into keywords
payload1 = {
    "keywords": "Microbiologist",
    "location": "India",
    "resultsonpage": 5
}

def test_payload(name, payload):
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            print(f"[{name}] Total jobs: {len(jobs)}")
            if len(jobs) > 0:
                print(f"First job: {jobs[0].get('title')} ({jobs[0].get('location')}) - source: {jobs[0].get('source')}")
        else:
            print(f"[{name}] Error: {response.text}")
    except Exception as e:
        print(f"[{name}] Exception: {e}")

test_payload("Country wide", payload1)
