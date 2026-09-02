import os
import datetime
from models import get_jobs, get_stats
from config import REPORTS_DIR

def generate_daily_report():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    report_filename = os.path.join(REPORTS_DIR, f"Job_Report_{today_str}.md")

    stats = get_stats()
    jobs = get_jobs(status="new", min_score=30, limit=100)

    lines = [
        f"# 📊 Daily Job Opportunities Report — {today_str}",
        "",
        "## Summary Metrics",
        f"- **Total Discovered:** {stats['total_found']}",
        f"- **Unapplied / New:** {stats['new_jobs']}",
        f"- **Applied Jobs:** {stats['applied_jobs']}",
        f"- **Full-Time Opportunities:** {stats['full_times']}",
        f"- **Internship Opportunities:** {stats['internships']}",
        "",
        "---",
        "",
        "## 🎯 Top Priority Job Openings",
        ""
    ]

    if not jobs:
        lines.append("*No new unapplied jobs found matching the minimum score threshold.*")
    else:
        lines.append("| Match | Role | Company | Location Priority | Type | Platform | Link |")
        lines.append("|:-----:|:-----|:--------|:-----------------:|:----:|:---------|:----|")
        for j in jobs:
            loc = j.get("location") or "India"
            p_badge = f"P{j.get('location_priority')}"
            link = f"[Apply Now]({j['url']})"
            lines.append(f"| **{j['match_score']}%** | {j['title']} | **{j['company']}** | {p_badge} ({loc}) | {j['job_type']} | {j['platform']} | {link} |")

    lines.append("")
    lines.append("---")
    lines.append(f"\n*Report generated automatically at {datetime.datetime.now().strftime('%H:%M:%S')}*")

    content = "\n".join(lines)
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"📝 Daily report saved to {report_filename}")
    return report_filename

if __name__ == "__main__":
    generate_daily_report()
