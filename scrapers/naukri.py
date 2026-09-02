from scrapers.base import BaseScraper
import urllib.parse
import json

class NaukriScraper(BaseScraper):
    def __init__(self):
        super().__init__("Naukri")
        self.session.headers.update({
            "appid": "109",
            "systemid": "Naukri"
        })

    def search(self, keywords="software engineer fresher", location="india"):
        jobs = []
        encoded_keywords = keywords.lower().replace(" ", "-")
        
        # Naukri's public JSON API endpoint with experience=0 for freshers
        url = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=cloudSearch&keywords={encoded_keywords}&experience=0&seoKey={encoded_keywords}-jobs&pageNo=1"

        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                job_details = data.get("jobDetails", [])
                
                for item in job_details:
                    title = item.get("title", "")
                    company = item.get("companyName", "")
                    loc = item.get("placeholders", [{}])[0].get("label", location)
                    job_url = "https://www.naukri.com" + item.get("jdURL", "")
                    salary = item.get("placeholders", [{}, {}])[1].get("label", "Not Disclosed") if len(item.get("placeholders", [])) > 1 else "Not Disclosed"
                    desc = item.get("jobDescription", "")
                    
                    if title and job_url:
                        jobs.append({
                            "title": title,
                            "company": company,
                            "location": loc,
                            "url": job_url,
                            "platform": "Naukri",
                            "salary": salary,
                            "posted_date": "Recently",
                            "description": desc or f"{title} role at {company}"
                        })
        except Exception as e:
            print(f"[Naukri] Exception: {e}")

        return jobs
