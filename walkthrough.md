# Job Hunter Agent — Walkthrough & User Guide

We have successfully built and launched your **Job Hunter Agent** in `c:\Users\zamba\OneDrive\Desktop\TEMP\Dump\REsumes\job-hunter`!

The system has already scraped, matched, and populated **342 active job opportunities** (178 Internships & 164 Full-Time Roles) sorted by your preferred locations and match score.

---

## 🎨 Web Dashboard Preview

The dashboard is running live locally at:
👉 **[http://localhost:5000](http://localhost:5000)**

![Job Dashboard Screen](file:///C:/Users/zamba/.gemini/antigravity-ide/brain/c0804275-22d2-4a77-bb72-e3b4d9c9b343/job_dashboard_1786268831117.png)

---

## 🔥 Key Features Implemented

1. **📍 Strict Location Preference Ranking:**
   - **Priority 1:** Nashik
   - **Priority 2:** Pune
   - **Priority 3:** Mumbai
   - **Priority 4:** Remote / Work From Home
   - **Priority 5:** Pan-India

2. **🎓 Role & Type Separation:**
   - Interactive dropdown filters to separate **Full-Time** roles from **Internships**.
   - Filtered for freshers and 0–1 year entry-level roles.

3. **🎯 Match Scoring Engine:**
   - Automatically scores every job (0% – 100%) against your skills (Python, C++, JS/TS, React, Node, FastAPI, RAG, Qdrant, Docker, AWS, etc.).

4. **⚡ One-Click Apply & Manual Tracking:**
   - Click **Apply Now ↗** to open the job URL directly in your browser.
   - Click **Mark Applied** to move jobs out of your "New / Unapplied" list.

5. **🕒 Both Scheduled & Manual Triggers:**
   - Click **"Find New Jobs Now"** in the top right of the web dashboard to trigger an instant scrape.
   - Run background automated scheduler via CLI.

---

## 💻 CLI Commands

You can run any of these commands from `c:\Users\zamba\OneDrive\Desktop\TEMP\Dump\REsumes\job-hunter`:

```bash
# 1. Start Web Dashboard (Default)
python main.py serve

# 2. Run Job Scraper Manually (Command Line)
python main.py run

# 3. Start Background Scheduler (Runs automatically every 4 hours)
python main.py schedule

# 4. Generate Daily Markdown Report
python main.py report
```

---

## 📁 Daily Markdown Reports

A daily summary report is saved to `c:\Users\zamba\OneDrive\Desktop\TEMP\Dump\REsumes\job-hunter\reports\Job_Report_2026-08-09.md` listing top 100% matched jobs in markdown table format.
