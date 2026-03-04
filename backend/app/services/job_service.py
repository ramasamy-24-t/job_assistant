import os
import requests
from app.services.ats_engine import ATSEngine

class JobService:
    @staticmethod
    def fetch_indeed_jobs(role: str, location: str, api_key: str):
        url = "https://indeed12.p.rapidapi.com/jobs/search"
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "indeed12.p.rapidapi.com"
        }
        
        target_city = location.split(',')[0].strip()
        params = {"query": role, "location": target_city, "locality": "in"}
        
        try:
            print(f"DEBUG: Starting request to Indeed API for '{role}' in '{target_city}'...")
            import time
            start = time.time()
            response = requests.get(url, headers=headers, params=params)
            end = time.time()
            print(f"DEBUG: Indeed API returned {response.status_code} in {end - start:.2f} seconds.")
            
            if response.status_code == 200:
                data = response.json()
                hits = data.get("hits", [])
                
                formatted_jobs = []
                for j in hits:
                    formatted_job = {
                        "id": j.get("id"),
                        "title": j.get("title"),
                        "company": j.get("company_name"),
                        "location": j.get("location"),
                        # Indeed12 API doesn't return full snippets in search, using title
                        "snippet": f"Role: {j.get('title')} at {j.get('company_name')}", 
                        "salary": "N/A",
                        "link": f"https://in.indeed.com{j.get('link')}",
                        "source": "Indeed",
                        "type": "Full-time", # API does not specify
                        "updated": j.get("formatted_relative_time")
                    }
                    
                    # Try to format salary if it exists
                    sal = j.get("salary")
                    if sal and isinstance(sal, dict):
                        sal_min = sal.get("min")
                        sal_max = sal.get("max")
                        sal_type = sal.get("type", "").lower()
                        if sal_min and sal_max:
                            formatted_job["salary"] = f"₹{sal_min} - ₹{sal_max} {sal_type}"
                        elif sal_min:
                            formatted_job["salary"] = f"₹{sal_min} {sal_type}"
                            
                    formatted_jobs.append(formatted_job)
                        
                return formatted_jobs
            else:
                print(f"Indeed API error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Failed to fetch from Indeed: {e}")
            return []

    @staticmethod
    def fetch_adzuna_jobs(role: str, location: str, app_id: str, app_key: str):
        url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
        target_city = location.split(',')[0].strip()
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": 20,
            "what": role,
            "where": target_city
        }
        
        try:
            print(f"DEBUG: Starting request to Adzuna API for '{role}' in '{target_city}'...")
            import time
            start = time.time()
            response = requests.get(url, params=params)
            end = time.time()
            print(f"DEBUG: Adzuna API returned {response.status_code} in {end - start:.2f} seconds.")
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                formatted_jobs = []
                for j in results:
                    salary_str = "N/A"
                    min_sal = j.get("salary_min")
                    max_sal = j.get("salary_max")
                    if min_sal and max_sal:
                        salary_str = f"₹{int(min_sal):,} - ₹{int(max_sal):,} Yearly"
                    elif min_sal:
                        salary_str = f"₹{int(min_sal):,} Yearly"

                    formatted_jobs.append({
                        "id": str(j.get("id")),
                        "title": j.get("title"),
                        "company": j.get("company", {}).get("display_name", "Confidential"),
                        "location": j.get("location", {}).get("display_name", location),
                        "snippet": j.get("description", ""),
                        "salary": salary_str,
                        "link": j.get("redirect_url"),
                        "source": "Adzuna",
                        "type": j.get("contract_time", "Full-time").replace("_", " ").title(),
                        "updated": j.get("created")
                    })
                        
                return formatted_jobs
            else:
                print(f"Adzuna API error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Failed to fetch from Adzuna: {e}")
            return []

    @staticmethod
    def fetch_and_rank_jobs(resume_text: str = None, parsed_json: dict = None, role: str = "", locations: list = None, provider: str = "rapidapi"):
        """
        Fetches live jobs from Jooble and ranks them based on ATS score against the given resume.
        Returns the top 20 jobs with scoring metadata.
        """
        if not locations:
            locations = ["Remote"]
            
        # Fallback if parsed json is empty
        if not parsed_json:
             from app.services.resume_parser import ResumeParserService
             parsed_json = ResumeParserService.parse_resume_text(resume_text or "")

        # Fetch from Provider concurrently
        import concurrent.futures
        
        all_fetched_jobs = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_loc = {}
            for loc in locations[:3]:
                if provider.lower() == "adzuna":
                    app_id = os.environ.get('ADZUNA_APP_ID')
                    app_key = os.environ.get('ADZUNA_APP_KEY')
                    if not app_id or not app_key:
                        raise ValueError("Missing ADZUNA_APP_ID or ADZUNA_APP_KEY environment variables")
                    future_to_loc[executor.submit(JobService.fetch_adzuna_jobs, role, loc, app_id, app_key)] = loc
                else: # Default to RapidAPI / Indeed
                    api_key = os.environ.get('RAPID_API')
                    if not api_key:
                        raise ValueError("Missing RAPID_API environment variable")
                    future_to_loc[executor.submit(JobService.fetch_indeed_jobs, role, loc, api_key)] = loc
            
            for future in concurrent.futures.as_completed(future_to_loc):
                try:
                    jobs = future.result()
                    all_fetched_jobs.extend(jobs)
                except Exception as exc:
                    loc = future_to_loc[future]
                    print(f"Location {loc} generated an exception: {exc}")
            
        # Deduplicate jobs by ID just in case
        seen_ids = set()
        unique_jobs = []
        for j in all_fetched_jobs:
            jid = j.get('id')
            if jid not in seen_ids:
                seen_ids.add(jid)
                unique_jobs.append(j)

        ranked_jobs = []
        for job in unique_jobs:
            desc = job.get("snippet", "") + " " + job.get("title", "")
            
            # Calculate score using the ATSEngine
            score_data = ATSEngine.calculate_ats_score(
                parsed_resume=parsed_json,
                job_description_text=desc
            )
            
            job_formatted = {
                "id": job.get("id"),
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "requirements": job.get("snippet"),
                "salary": job.get("salary", "N/A"),
                "link": job.get("link"),
                "source": job.get("source"),
                "type": job.get("type"),
                "updated": job.get("updated"),
                "ats_match_score": score_data["score"],
                "ats_details": {
                    "missing_skills": score_data["missing_skills"],
                    "matched_skills": score_data["matched_skills"],
                    "experience_gap": score_data["experience_gap"]
                }
            }
            ranked_jobs.append(job_formatted)
            
        # Sort jobs by ats_match_score in descending order
        ranked_jobs = sorted(ranked_jobs, key=lambda x: x["ats_match_score"], reverse=True)
        
        return ranked_jobs[:20]
