import time
from app.services.ats_engine import ATSEngine

text = "Role: Assistant Professor - Microbiology at Rathinam International Public School"

print("Starting ATS Engine extraction...")
start = time.time()
reqs = ATSEngine._extract_job_requirements(text)
end = time.time()
print(f"Extraction took {end-start:.2f} seconds.")
print(reqs)
