import time
import schedule
from scrapers.runner import run_all_scrapers

def job_routine():
    print(f"\n[Scheduler] ⏰ Starting automated job hunt cycle at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        results = run_all_scrapers()
        print(f"[Scheduler] ✅ Finished cycle. New jobs found: {results.get('total_new', 0)}")
    except Exception as e:
        print(f"[Scheduler] ⚠️ Error during scheduled run: {e}")

def start_scheduler(interval_hours=4):
    print(f"🕒 Background scheduler initialized (Running every {interval_hours} hours).")
    # Run once immediately
    job_routine()
    
    schedule.every(interval_hours).hours.do(job_routine)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_scheduler(interval_hours=4)
