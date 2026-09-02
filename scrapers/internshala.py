from bs4 import BeautifulSoup
from scrapers.base import BaseScraper
import urllib.parse

class InternshalaScraper(BaseScraper):
    def __init__(self):
        super().__init__("Internshala")

    def search(self, keywords="software engineer", location=""):
        jobs = []
        # Internshala supports both internships and fresher jobs
        categories = ["internships", "fresher-jobs"]
        
        for category in categories:
            query = keywords.lower().replace(" ", "-")
            if category == "internships":
                url = f"https://internshala.com/internships/keywords-{query}"
            else:
                url = f"https://internshala.com/fresher-jobs/keywords-{query}"

            html = self.fetch_url(url)
            if not html:
                continue

            soup = BeautifulSoup(html, "html.parser")
            containers = soup.select(".individual_internship")

            for container in containers:
                try:
                    title_elem = container.select_one(".job-internship-name, .heading_4_5")
                    company_elem = container.select_one(".company-name, .heading_6")
                    location_elem = container.select_one(".location_link, #location_names")
                    link_elem = container.select_one("a[href*='/internship/detail/'], a[href*='/job/detail/']")
                    salary_elem = container.select_one(".stipend, .salary")

                    if not title_elem or not link_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
                    loc = location_elem.get_text(strip=True) if location_elem else location or "India"
                    href = link_elem.get("href", "")
                    full_url = urllib.parse.urljoin("https://internshala.com", href)
                    salary = salary_elem.get_text(strip=True) if salary_elem else "Not specified"
                    
                    job_type = "Internship" if category == "internships" else "Full Time"

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": loc,
                        "url": full_url,
                        "platform": "Internshala",
                        "salary": salary,
                        "job_type": job_type,
                        "posted_date": "Recently",
                        "description": f"{title} position at {company} in {loc}"
                    })
                except Exception as e:
                    continue

        return jobs
