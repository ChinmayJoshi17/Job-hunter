import sys

# Ensure UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from scrapers.internshala import InternshalaScraper
from scrapers.linkedin import LinkedInScraper
from scrapers.naukri import NaukriScraper
from scrapers.google_jobs import GoogleJobsScraper
from scrapers.indeed import IndeedScraper
from scrapers.wellfound import WellfoundScraper
from scrapers.glassdoor import GlassdoorScraper
from matcher import process_raw_job
from models import save_job, init_db

ALL_SCRAPERS = [
    InternshalaScraper(),
    LinkedInScraper(),
    NaukriScraper(),
    GoogleJobsScraper(),
    IndeedScraper(),
    WellfoundScraper(),
    GlassdoorScraper()
]

# Targeted specifically for 0-1 year freshers & entry-level roles
FRESHER_TARGET_KEYWORDS = [
    "Junior Software Engineer",
    "Software Engineer Fresher",
    "Associate Software Engineer",
    "Junior Full Stack Developer",
    "Junior AI Engineer",
    "Software Engineer Trainee",
    "Junior Backend Engineer",
    "Python Developer Fresher"
]

def run_all_scrapers(keywords_list=None, location="India"):
    init_db()
    if not keywords_list:
        keywords_list = FRESHER_TARGET_KEYWORDS

    total_new = 0
    total_found = 0

    print(f"[*] Starting job search across {len(ALL_SCRAPERS)} platforms for Fresher (0-1 yrs) roles...")

    for scraper in ALL_SCRAPERS:
        print(f"\n[*] Running {scraper.platform_name} Scraper...")
        platform_found = 0
        platform_new = 0

        for keyword in keywords_list:
            try:
                raw_jobs = scraper.search(keywords=keyword, location=location)
                for raw in raw_jobs:
                    processed = process_raw_job(raw)
                    if processed:  # Only save if passed strict 0-1 year experience filter
                        platform_found += 1
                        if save_job(processed):
                            platform_new += 1
            except Exception as e:
                print(f"[!] Error running {scraper.platform_name} for '{keyword}': {e}")

        print(f"[+] {scraper.platform_name}: Found {platform_found} entry-level listings ({platform_new} new saved)")
        total_found += platform_found
        total_new += platform_new

    print(f"\n[+] Search Complete! Found {total_found} fresher/entry-level opportunities ({total_new} new added to database).")
    return {"total_found": total_found, "total_new": total_new}

if __name__ == "__main__":
    run_all_scrapers()
