import re
from app.services.resume_parser import ResumeParserService

class ATSEngine:
    
    @staticmethod
    def _extract_job_requirements(job_text: str) -> dict:
        """
        Processes a Job Description text to extract required skills, keywords, and experience.
        """
        text_lower = job_text.lower()
        
        # 1. Extract required skills
        job_skills = set()
        for skill in ResumeParserService.SKILLS_DICT:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                job_skills.add(skill)
                
        # 2. Extract keywords
        job_keywords = set()
        for kw in ResumeParserService.KEYWORDS_DICT:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                job_keywords.add(kw)
                
        # 3. Detect required experience (Looking for "X+ years", "minimum of X years", etc.)
        req_exp = 0
        exp_matches = re.findall(r'(?:minimum(?: of)?|at least|\b)(\d+)\+?\s*years?(?:\s+of)?\s+(?:professional\s+)?experience', text_lower)
        if exp_matches:
            try:
                req_exp = max([int(y) for y in exp_matches])
            except ValueError:
                pass
                
        # Sometimes it says "5 years of Python experience" without standard phrasing,
        # but the simple regex above catches the most common explicit "years of experience".
        
        return {
            "required_skills": list(job_skills),
            "required_keywords": list(job_keywords),
            "required_years": req_exp
        }

    @staticmethod
    def calculate_ats_score(parsed_resume: dict, job_description_text: str) -> dict:
        """
        Calculates ATS matching score based on formula:
        - Skill match (50%)
        - Keyword overlap (30%)
        - Experience relevance (20%)
        """
        job_reqs = ATSEngine._extract_job_requirements(job_description_text)
        
        result = {
            "score": 0,
            "missing_skills": [],
            "matched_skills": [],
            "experience_gap": "No gap"
        }
        
        # Extract parsed resume data
        resume_skills = set(parsed_resume.get("skills", []))
        resume_keywords = set(parsed_resume.get("keywords", []))
        resume_years = parsed_resume.get("years_of_experience", 0)
        
        # 1. Skill Match (50% weight)
        req_skills = set(job_reqs["required_skills"])
        if not req_skills:
            # If Job description has no distinct identifiable skills from our dict,
            # we don't penalize the user, we just grant full points.
            skill_score = 50.0
        else:
            matched_skills = req_skills.intersection(resume_skills)
            result["matched_skills"] = list(matched_skills)
            result["missing_skills"] = list(req_skills.difference(resume_skills))
            
            skill_score = (len(matched_skills) / len(req_skills)) * 50.0
            
        # 2. Keyword Overlap (30% weight)
        req_keywords = set(job_reqs["required_keywords"])
        if not req_keywords:
            keyword_score = 30.0 # Full points if no keywords specified
        else:
            matched_keywords = req_keywords.intersection(resume_keywords)
            keyword_score = (len(matched_keywords) / len(req_keywords)) * 30.0
            
        # 3. Experience Relevance (20% weight)
        req_years = job_reqs["required_years"]
        if req_years == 0:
            exp_score = 20.0 # Entry level / Unspecified
            result["experience_gap"] = "Unspecified Experience Requirement"
        else:
            if resume_years >= req_years:
                exp_score = 20.0
                result["experience_gap"] = "Meets or exceeds required experience"
            else:
                # Partial score if they have some experience but not enough
                exp_score = (resume_years / req_years) * 20.0
                diff = req_years - resume_years
                result["experience_gap"] = f"{diff} year(s) short"
                
        # Total Score
        total_score = skill_score + keyword_score + exp_score
        result["score"] = round(total_score, 2)
        
        # Provide extra context if we didn't extract any structured job info
        if not req_skills and not req_keywords and req_years == 0:
            result["note"] = "Job description lacks structured keywords; score defaulted to 100."
            
        return result
