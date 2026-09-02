import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DB_PATH = os.path.join(DATA_DIR, "jobs.db")

# User Profile Context for Matching & Scoring
USER_PROFILE = {
    "name": "Toshal Zambare",
    "email": "toshalzambare1@gmail.com",
    "education": "B.E. Artificial Intelligence & Data Science",
    "location": "Nashik, Maharashtra",
    "primary_skills": [
        "python", "c++", "javascript", "typescript", "react", "react native",
        "node.js", "express", "fastapi", "flask", "postgresql", "mongodb",
        "redis", "docker", "aws", "rest api", "websockets", "data structures",
        "algorithms", "langchain", "rag", "qdrant", "vector database"
    ],
    "secondary_skills": [
        "html5", "css3", "flutter", "dart", "java", "sql", "linux",
        "unity", "c#", "opencv", "tensorflow", "pytorch", "minio", "celery"
    ]
}

# Location Preferences in Priority Order
LOCATION_PREFERENCE_ORDER = [
    "Nashik",
    "Pune",
    "Mumbai",
    "Remote",
    "India"
]

# Roles Targeted
TARGET_ROLES = [
    "Software Development Engineer",
    "Software Engineer",
    "Full Stack Developer",
    "Backend Developer",
    "Frontend Developer",
    "AI Engineer",
    "Machine Learning Engineer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Python Developer"
]

# Experience Filter: Freshers & 0-1 Year Experience
EXPERIENCE_LEVELS = ["fresher", "0-1 years", "internship", "entry level"]

# Scraper Settings
SCRAPER_SETTINGS = {
    "request_delay_seconds": 3,
    "max_pages_per_platform": 5,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
