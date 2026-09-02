import time
import requests
from config import SCRAPER_SETTINGS

class BaseScraper:
    def __init__(self, platform_name):
        self.platform_name = platform_name
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": SCRAPER_SETTINGS["user_agent"],
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        })
        
    def fetch_url(self, url, params=None):
        try:
            time.sleep(SCRAPER_SETTINGS["request_delay_seconds"])
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print(f"[{self.platform_name}] HTTP {response.status_code} for {url}")
                return None
        except Exception as e:
            print(f"[{self.platform_name}] Error fetching {url}: {e}")
            return None

    def search(self, keywords, location):
        raise NotImplementedError("Subclasses must implement search()")
