from bs4 import BeautifulSoup
from scrapers.base import BaseScraper
import urllib.parse

class GlassdoorScraper(BaseScraper):
    def __init__(self):
        super().__init__("Glassdoor")

    def search(self, keywords="Software Engineer", location="India"):
        jobs = []
        encoded_keywords = urllib.parse.quote(keywords)
        url = f"https://www.glassdoor.co.in/Job/india-{encoded_keywords}-jobs-SRCH_IL.0,5_IN115_KO6,{6+len(keywords)}.htm"

        html = self.fetch_url(url)
        if not html:
            return jobs

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".JobsList_jobListItem__wjTHv, li[data-test='jobListing']")

        for card in cards:
            try:
                title_elem = card.select_one("a[data-test='job-title'], .JobCard_jobTitle___iAOf")
                company_elem = card.select_one(".EmployerProfile_employerName__dW22u, .EmployerProfile_compactEmployerName__LE242")
                location_elem = card.select_one("[data-test='emp-location'], .JobCard_location__r02WZ")

                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                company = company_elem.get_text(strip=True) if company_elem else "Company"
                loc = location_elem.get_text(strip=True) if location_elem else location
                href = title_elem.get("href", "")
                full_url = urllib.parse.urljoin("https://www.glassdoor.co.in", href)

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": loc,
                    "url": full_url,
                    "platform": "Glassdoor",
                    "posted_date": "Recently",
                    "description": f"{title} position at {company}"
                })
            except Exception:
                continue

        return jobs
