from bs4 import BeautifulSoup
from scrapers.base import BaseScraper
import urllib.parse

class WellfoundScraper(BaseScraper):
    def __init__(self):
        super().__init__("Wellfound")

    def search(self, keywords="Software Engineer", location="India"):
        jobs = []
        encoded_keywords = urllib.parse.quote(keywords)
        url = f"https://wellfound.com/jobs?q={encoded_keywords}"

        html = self.fetch_url(url)
        if not html:
            return jobs

        soup = BeautifulSoup(html, "html.parser")
        listings = soup.select("[data-test='JobListItem'], .styles_jobListItem__")

        for item in listings:
            try:
                title_elem = item.select_one("a[class*='title'], h2")
                company_elem = item.select_one("h3, [class*='startupName']")
                location_elem = item.select_one("[class*='location']")

                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                company = company_elem.get_text(strip=True) if company_elem else "Startup"
                loc = location_elem.get_text(strip=True) if location_elem else location
                href = title_elem.get("href", "")
                full_url = urllib.parse.urljoin("https://wellfound.com", href) if href else url

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": loc,
                    "url": full_url,
                    "platform": "Wellfound",
                    "posted_date": "Recently",
                    "description": f"{title} opportunity at {company}"
                })
            except Exception:
                continue

        return jobs
