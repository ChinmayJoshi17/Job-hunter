# 🚀 Job Hunter Agent

An automated job discovery, match scoring, and tracking agent designed to scrape top job platforms, prioritize listings by location preference (Nashik → Pune → Mumbai → Remote → India), score relevancy against your tech stack, and present opportunities through an interactive Web Dashboard and daily Markdown reports.

---

## 🌟 Features

- **🌐 Multi-Platform Aggregation:** Automatically searches job openings across **LinkedIn**, **Internshala**, **Naukri**, **Google Jobs**, **Indeed**, **Wellfound (AngelList)**, and **Glassdoor**.
- **📍 Location Priority Ranking:**
  1. **Priority 1:** Nashik
  2. **Priority 2:** Pune
  3. **Priority 3:** Mumbai
  4. **Priority 4:** Remote / Work From Home
  5. **Priority 5:** Pan-India / Other
- **🎓 Role Type Separation:** Filter easily between **Full Time** fresher roles and **Internships**.
- **🎯 Intelligent Match Scoring (0% – 100%):** Evaluates role titles and job descriptions against your skills (Python, C++, JS/TS, React, Node.js, FastAPI, RAG, Qdrant, Docker, AWS, etc.).
- **⚡ One-Click Apply & Manual Tracking:** Opens job URLs in your browser and lets you mark listings as **Applied**, **Saved**, or **Ignored** to avoid duplicate applications.
- **🔄 Flexible Execution:** Supports both on-demand manual triggers via the Web UI / CLI and background scheduled runs (e.g., every 4 hours).
- **📝 Daily Markdown Reports:** Generates structured summary reports sorted by match score.

---

## 🏗️ Architecture & Project Structure

```
job-hunter/
├── main.py              # CLI Entry Point (run, serve, schedule, report)
├── config.py            # User profile, skills & location priority settings
├── models.py            # SQLite database schema & helper methods
├── matcher.py           # Job scoring algorithm & location priority engine
├── scheduler.py         # Automated background cron runner
├── reporter.py          # Daily Markdown report generator
├── app.py               # Flask Web Dashboard REST API & server
├── requirements.txt     # Python dependencies
├── scrapers/            # Platform-specific scrapers
│   ├── base.py
│   ├── linkedin.py
│   ├── internshala.py
│   ├── naukri.py
│   ├── google_jobs.py
│   ├── indeed.py
│   ├── wellfound.py
│   ├── glassdoor.py
│   └── runner.py
├── templates/
│   └── index.html       # Single-Page Web Dashboard UI
├── static/
│   └── style.css        # Dark mode styling (TokyoNight palette)
├── reports/             # Generated daily Markdown reports
└── data/
    └── jobs.db          # SQLite database storage
```

---

## 📋 Prerequisites

- **Python 3.10+** installed on your system
- `pip` package manager

---

## ⚙️ Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd job-hunter
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Profile (Optional):**
   Open `config.py` to customize your target skills, roles, or location priority:
   ```python
   USER_PROFILE = {
       "name": "Your Name",
       "primary_skills": ["python", "c++", "javascript", "react", "node.js", ...],
   }
   ```

---

## 🚀 How to Run

### 1. Launch the Web Dashboard (Recommended)

Run the Flask web app to browse jobs interactively:

```bash
python main.py serve
```

Open **`http://localhost:5000`** in your web browser.

From the web dashboard, you can:
- Browse 300+ scraped jobs with live filters (Full Time vs Internship, Location, Match Score).
- Click **Apply Now ↗** to open job links directly.
- Click **Mark Applied** to update your job status.
- Click **"Find New Jobs Now"** at the top right to trigger a fresh scrape across all platforms.

---

### 2. Run Job Discovery Once (CLI)

To scrape all platforms from the terminal without starting the web server:

```bash
python main.py run
```

---

### 3. Run Automated Background Scheduler

To keep the agent running in the background and discovering new jobs automatically every 4 hours:

```bash
python main.py schedule
```

---

### 4. Generate Daily Markdown Report

To generate a clean Markdown report of top-matched jobs saved in `reports/Job_Report_YYYY-MM-DD.md`:

```bash
python main.py report
```

---

## 🛠️ CLI Quick Reference

| Command | Action |
|:--------|:-------|
| `python main.py serve` | Starts Web Dashboard at `http://localhost:5000` |
| `python main.py run` | Scrapes all job platforms immediately |
| `python main.py schedule` | Runs continuous background scheduler (every 4 hrs) |
| `python main.py report` | Generates a daily Markdown summary report |

---

## 🤝 Contributing & License

Built with Python, Flask, SQLite, BeautifulSoup4, and HTML/CSS. Open-source under MIT License.
