import hashlib
import re
from config import USER_PROFILE, LOCATION_PREFERENCE_ORDER, TARGET_ROLES

SENIOR_TITLE_KEYWORDS = [
    "senior", "sr.", "sr ", "lead", "manager", "architect", "principal", "staff",
    "head of", "director", "vp", "vice president", "executive", "expert", "consultant",
    "team lead", "tech lead", "technical lead", "engineering manager", "3+", "4+", "5+", "6+", "7+", "8+", "10+"
]

SENIOR_EXP_PATTERNS = [
    r"\b(3|4|5|6|7|8|9|10)\s*\+\s*years?\b",
    r"\b(3|4|5|6|7|8|9|10)\s*-\s*(5|6|7|8|9|10|12)\s*years?\b",
    r"\bminimum\s+(3|4|5|6|7|8)\s+years?\b",
    r"\bat\s+least\s+(3|4|5|6|7|8)\s+years?\b",
    r"\b(3|4|5|6|7|8)\+\s*yrs\b"
]

def generate_job_id(title, company, url):
    raw = f"{title.lower().strip()}_{company.lower().strip()}_{url.strip()}"
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

def is_senior_or_experienced(title, description=""):
    title_lower = title.lower()
    desc_lower = description.lower()

    # Check title for senior keywords
    for keyword in SENIOR_TITLE_KEYWORDS:
        if keyword in title_lower:
            return True

    # Check description for 3+ years experience requirements
    for pattern in SENIOR_EXP_PATTERNS:
        if re.search(pattern, desc_lower):
            return True

    return False

def get_location_priority(location_str):
    if not location_str:
        return 99
        
    loc = location_str.lower()
    
    if "nashik" in loc:
        return 1
    elif "pune" in loc:
        return 2
    elif "mumbai" in loc or "bombay" in loc:
        return 3
    elif "remote" in loc or "work from home" in loc or "wfh" in loc:
        return 4
    elif "india" in loc:
        return 5
    else:
        return 6

def determine_job_type(title, description=""):
    combined = f"{title} {description}".lower()
    if "intern" in combined or "trainee" in combined or "apprentice" in combined or "stipend" in combined:
        return "Internship"
    return "Full Time"

def calculate_match_score(title, description=""):
    score = 0
    title_lower = title.lower()
    desc_lower = description.lower()

    # If it's explicitly a fresher / entry level role, give bonus
    if any(k in title_lower or k in desc_lower for k in ["fresher", "junior", "jr.", "entry level", "associate", "trainee", "intern"]):
        score += 25
    
    # Target role bonus (up to 40 pts)
    for role in TARGET_ROLES:
        role_words = role.lower().split()
        if all(w in title_lower for w in role_words):
            score += 40
            break
        elif any(w in title_lower for w in role_words if len(w) > 3):
            score += 20
            
    # Primary skills bonus (up to 40 pts)
    primary_matches = sum(1 for skill in USER_PROFILE["primary_skills"] if skill in title_lower or skill in desc_lower)
    score += min(primary_matches * 5, 40)
    
    # Secondary skills bonus (up to 20 pts)
    secondary_matches = sum(1 for skill in USER_PROFILE["secondary_skills"] if skill in title_lower or skill in desc_lower)
    score += min(secondary_matches * 3, 20)
    
    return min(max(score, 10), 100)

def process_raw_job(raw_job):
    title = raw_job.get("title", "")
    company = raw_job.get("company", "")
    location = raw_job.get("location", "")
    url = raw_job.get("url", "")
    description = raw_job.get("description", "")
    platform = raw_job.get("platform", "Unknown")
    salary = raw_job.get("salary", "Not Disclosed")
    posted_date = raw_job.get("posted_date", "Recently")
    
    # Strict Experience Filter: Discard any senior/experienced positions
    if is_senior_or_experienced(title, description):
        return None

    job_id = generate_job_id(title, company, url)
    location_priority = get_location_priority(location)
    job_type = raw_job.get("job_type") or determine_job_type(title, description)
    match_score = calculate_match_score(title, description)
    
    return {
        "id": job_id,
        "title": title,
        "company": company,
        "location": location,
        "location_priority": location_priority,
        "job_type": job_type,
        "platform": platform,
        "url": url,
        "description": description,
        "salary": salary,
        "posted_date": posted_date,
        "match_score": match_score
    }
