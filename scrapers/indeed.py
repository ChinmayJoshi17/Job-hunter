from bs4 import BeautifulSoup
from scrapers.base import BaseScraper
import urllib.parse

class IndeedScraper(BaseScraper):
    def __init__(self):
        super().__init__("Indeed")

    def search(self, keywords="Software Engineer", location="India"):
        jobs = []
        encoded_keywords = urllib.parse.quote(keywords)
        encoded_location = urllib.parse.quote(location)
        url = f"https://in.indeed.com/jobs?q={encoded_keywords}&l={encoded_location}"

        html = self.fetch_url(url)
        if not html:
            return jobs

        soup = BeautifulSoup(html, "html.parser")
        job_cards = soup.select(".job_seen_beacon, .result")

        for card in job_cards:
            try:
                title_elem = card.select_one("h2.jobTitle span, a.j4wing")
                company_elem = card.select_one("[data-testid='company-name'], .companyName")
                location_elem = card.select_one("[data-testid='text-location'], .companyLocation")
                link_elem = card.select_one("a[data-jk], h2.jobTitle a")

                if not title_elem or not link_elem:
                    continue

                title = title_elem.get_text(strip=True)
                company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
                loc = location_elem.get_text(strip=True) if location_elem else location
                jk = link_elem.get("data-jk") or link_elem.get("href", "")
                
                if jk.startswith("http"):
                    job_url = jk
                else:
                    job_url = f"https://in.indeed.com/viewjob?jk={jk}"

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": loc,
                    "url": job_url,
                    "platform": "Indeed",
                    "posted_date": "Recently",
                    "description": f"{title} position at {company} ({loc})"
                })
            except Exception:
                continue

        return jobs
