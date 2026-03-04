import os
import requests
from dotenv import load_dotenv
import json
import logging
from app import create_app
from app.services.job_service import JobService
from app.models.resume import Resume
from app.models.user import User

load_dotenv()
app = create_app()

with app.app_context():
    try:
        print("1. Fetching user and resume...")
        user = User.query.first()
        resume = Resume.query.filter_by(user_id=user.id).order_by(Resume.uploaded_at.desc()).first()
        
        print(f"2. Calling fetch_and_rank_jobs for {user.email}...")
        import time
        t1 = time.time()
        
        ranked_jobs = JobService.fetch_and_rank_jobs(
            resume_text=resume.raw_text,
            parsed_json=resume.parsed_json,
            role="Assistant Professor",
            locations=["Coimbatore", "Bangalore"]
        )
        t2 = time.time()
        print(f"3. Success! Ranked {len(ranked_jobs)} jobs in {t2-t1:.2f} seconds.")
    except Exception as e:
        print(f"Exception during ranking: {e}")
        import traceback
        traceback.print_exc()
