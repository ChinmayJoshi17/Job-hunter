import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from scrapers.runner import run_all_scrapers
from app import app
from scheduler import start_scheduler
from reporter import generate_daily_report
from models import init_db

def print_help():
    print("""
Job Hunter Agent CLI

Usage:
  python main.py run        Run all scrapers once to find new jobs
  python main.py serve      Launch the Web Dashboard (http://localhost:5000)
  python main.py schedule   Run the background scheduler (every 4 hours)
  python main.py report     Generate a Markdown report of new jobs
    """)

def main():
    init_db()
    if len(sys.argv) < 2:
        print_help()
        return

    cmd = sys.argv[1].lower()

    if cmd == "run":
        run_all_scrapers()
    elif cmd == "serve":
        print("Starting Job Hunter Web Dashboard on http://localhost:5000")
        app.run(host="0.0.0.0", port=5000, debug=False)
    elif cmd == "schedule":
        start_scheduler(interval_hours=4)
    elif cmd == "report":
        generate_daily_report()
    else:
        print(f"Unknown command: {cmd}")
        print_help()

if __name__ == "__main__":
    main()
