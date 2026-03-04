import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

rapid_api_key = os.environ.get('RAPID_API')

def fetch_indeed():
    url = "https://indeed12.p.rapidapi.com/company/Ubisoft/jobs" # User's snippet
    querystring = {"locality":"us","start":"1"}
    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "indeed12.p.rapidapi.com"
    }

    print("Fetching Indeed...")
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        with open('cached_indeed.json', 'w', encoding='utf-8') as f:
            json.dump(response.json(), f)
            print("Saved Indeed response to cached_indeed.json")
    else:
        print(f"Indeed Error {response.status_code}: {response.text}")

def fetch_linkedin():
    url = "https://linkedin-job-search-api.p.rapidapi.com/active-jb-1h" # User's snippet
    querystring = {"limit":"10","offset":"0","description_type":"text"} # Reduced limit to 10 for testing
    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "linkedin-job-search-api.p.rapidapi.com"
    }

    print("Fetching LinkedIn...")
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        with open('cached_linkedin.json', 'w', encoding='utf-8') as f:
            json.dump(response.json(), f)
            print("Saved LinkedIn response to cached_linkedin.json")
    else:
        print(f"LinkedIn Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    if not os.path.exists('cached_indeed.json'):
        fetch_indeed()
    else:
         print("Indeed cache already exists.")
         
    if not os.path.exists('cached_linkedin.json'):
         fetch_linkedin()
    else:
         print("LinkedIn cache already exists.")
