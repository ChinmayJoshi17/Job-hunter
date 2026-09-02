from bs4 import BeautifulSoup
from scrapers.base import BaseScraper
import urllib.parse

class GoogleJobsScraper(BaseScraper):
    def __init__(self):
        super().__init__("GoogleJobs")

    def search(self, keywords="Software Engineer", location="India"):
        jobs = []
        query = f"{keywords} jobs in {location}"
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded_query}&ibp=htl;jobs"

        html = self.fetch_url(url)
        if not html:
            return jobs

        soup = BeautifulSoup(html, "html.parser")
        job_nodes = soup.select("li, div[data-job-id]")

        for node in job_nodes:
            try:
                title_elem = node.select_one(".BjA2M, .P827Vb, font")
                company_elem = node.select_one(".vL2d1, .nA25bf")
                location_elem = node.select_one(".Qk80Jf")

                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                company = company_elem.get_text(strip=True) if company_elem else "Various Companies"
                loc = location_elem.get_text(strip=True) if location_elem else location

                # Build search link to job
                job_url = f"https://www.google.com/search?q={urllib.parse.quote(title + ' ' + company)}&ibp=htl;jobs"

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": loc,
                    "url": job_url,
                    "platform": "Google Jobs",
                    "posted_date": "Recently",
                    "description": f"{title} found via Google Jobs"
                })
            except Exception:
                continue

        return jobs
