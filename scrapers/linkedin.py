from bs4 import BeautifulSoup
from scrapers.base import BaseScraper
import urllib.parse

class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__("LinkedIn")

    def search(self, keywords="Software Engineer", location="India"):
        jobs = []
        encoded_keywords = urllib.parse.quote(keywords)
        encoded_location = urllib.parse.quote(location)
        
        # f_E=1,2 restricts search to Internship (1) and Entry Level (2) only on LinkedIn
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={encoded_keywords}&location={encoded_location}&f_E=1,2&start=0"

        html = self.fetch_url(url)
        if not html:
            return jobs

        soup = BeautifulSoup(html, "html.parser")
        job_cards = soup.find_all("li")

        for card in job_cards:
            try:
                title_elem = card.find("h3", class_="base-search-card__title")
                company_elem = card.find("h4", class_="base-search-card__subtitle")
                location_elem = card.find("span", class_="job-search-card__location")
                link_elem = card.find("a", class_="base-card__full-link")
                time_elem = card.find("time")

                if not title_elem or not link_elem:
                    continue

                title = title_elem.get_text(strip=True)
                company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
                loc = location_elem.get_text(strip=True) if location_elem else location
                job_url = link_elem.get("href", "").split("?")[0]
                posted_date = time_elem.get_text(strip=True) if time_elem else "Recently"

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": loc,
                    "url": job_url,
                    "platform": "LinkedIn",
                    "posted_date": posted_date,
                    "description": f"{title} opportunity at {company} in {loc}"
                })
            except Exception as e:
                continue

        return jobs
