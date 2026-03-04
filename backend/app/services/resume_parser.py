import re

class ResumeParserService:
    # Skill dictionary to match against
    SKILLS_DICT = {
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'php', 'swift', 'kotlin', 'rust',
        # Web Frameworks/Tech
        'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring boot', 'html', 'css', 'sass',
        # Cloud/DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ci/cd', 'linux', 'bash',
        # Databases
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'oracle',
        # Data/ML
        'machine learning', 'artificial intelligence', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch',
        # Tools
        'git', 'jira', 'agile', 'scrum', 'rest api', 'graphql', 'microservices'
    }
    
    # Generic keywords often found in resumes that are not strictly skills
    KEYWORDS_DICT = {
        'leadership', 'management', 'communication', 'problem solving', 'teamwork', 'analytical', 
        'project management', 'troubleshooting', 'mentoring', 'architecture', 'design patterns'
    }

    @staticmethod
    def parse_resume_text(text: str) -> dict:
        """
        Parses resume text using regex and dictionaries to extract structured information.
        """
        text_lower = text.lower()
        
        parsed_data = {
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "years_of_experience": 0,
            "keywords": []
        }
        
        parsed_data["skills"] = ResumeParserService._extract_skills(text_lower)
        parsed_data["keywords"] = ResumeParserService._extract_keywords(text_lower)
        parsed_data["years_of_experience"] = ResumeParserService._extract_years_of_experience(text_lower)
        parsed_data["education"] = ResumeParserService._extract_education(text_lower)
        
        # In a real NLP model, we would use NER (Named Entity Recognition) to segment 
        # experience descriptions and project descriptions. Here we use basic keyword finding 
        # or structure assumptions.
        parsed_data["experience"] = ResumeParserService._extract_experience_blocks(text_lower)
        parsed_data["projects"] = ResumeParserService._extract_project_blocks(text_lower)

        return parsed_data

    @staticmethod
    def _extract_skills(text_lower: str) -> list:
        found_skills = set()
        for skill in ResumeParserService.SKILLS_DICT:
            # Word boundary regex to match exact skill words like 'go' or 'react'
            # Escape skill to handle things like c++
            escaped_skill = re.escape(skill)
            if re.search(r'\b' + escaped_skill + r'\b', text_lower):
                found_skills.add(skill)
        return list(found_skills)
        
    @staticmethod
    def _extract_keywords(text_lower: str) -> list:
        found_keywords = set()
        for kw in ResumeParserService.KEYWORDS_DICT:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                found_keywords.add(kw)
        return list(found_keywords)

    @staticmethod
    def _extract_years_of_experience(text_lower: str) -> int:
        """
        Looks for patterns like '5+ years' or '5 years of experience'.
        Sums or takes the max depending on context, we take the max found to be safe.
        """
        exp_matches = re.findall(r'(\d+)\+?\s*years?(?:\s+of)?\s+(?:professional\s+)?experience', text_lower)
        
        if exp_matches:
            try:
                # Convert string matches to ints and find max
                years = [int(y) for y in exp_matches]
                return max(years)
            except ValueError:
                pass
        return 0

    @staticmethod
    def _extract_education(text_lower: str) -> list:
        """
        Looks for common degree formats.
        """
        found_education = set()
        degrees = [
            'bachelor', 'master', 'phd', 'b.s.', 'm.s.', 'b.a.', 'b.sc', 'm.sc', 'doctorate',
            'b.tech', 'm.tech', 'bachelors', 'masters'
        ]
        degree_patterns = [r'\b' + re.escape(deg) + r'\b' for deg in degrees]
        
        for pattern in degree_patterns:
            if re.search(pattern, text_lower):
                # Clean up the name for the final array
                clean_name = pattern.replace('\\b', '').replace('\\', '').title()
                found_education.add(clean_name)
                
        return list(found_education)

    @staticmethod
    def _extract_experience_blocks(text_lower: str) -> list:
        """
        Placeholder for experience block extraction.
        A real implementation would look for Dates (e.g. 2018 - 2021) and company names
        near headers like 'experience' or 'work history'.
        """
        # For Phase 1 without a complex spaCy model, we can just indicate 
        # whether 'experience' section was found, but returning a structured block 
        # is hard with pure regex without reliable formatting boundaries.
        if "experience" in text_lower or "employment" in text_lower or "work history" in text_lower:
            return ["Detected Work Experience Section (Raw text parsing requires layout understanding)"]
        return []

    @staticmethod
    def _extract_project_blocks(text_lower: str) -> list:
        """
        Placeholder for project block extraction.
        """
        if "projects" in text_lower or "personal projects" in text_lower:
            return ["Detected Projects Section"]
        return []

