from flask import Flask, render_template, jsonify, request
from models import get_jobs, update_job_status, get_stats, init_db
from scrapers.runner import run_all_scrapers
import threading

app = Flask(__name__)
init_db()

is_scraping = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/jobs", methods=["GET"])
def api_get_jobs():
    job_type = request.args.get("type", None)
    if job_type == "all":
        job_type = None
        
    status = request.args.get("status", None)
    if status == "all":
        status = None
        
    min_score = int(request.args.get("min_score", 0))
    limit = int(request.args.get("limit", 150))
    
    jobs = get_jobs(job_type=job_type, status=status, min_score=min_score, limit=limit)
    return jsonify({"success": True, "jobs": jobs, "count": len(jobs)})

@app.route("/api/jobs/<job_id>/status", methods=["POST"])
def api_update_status(job_id):
    data = request.get_json() or {}
    new_status = data.get("status", "applied")
    update_job_status(job_id, new_status)
    return jsonify({"success": True, "job_id": job_id, "new_status": new_status})

@app.route("/api/stats", methods=["GET"])
def api_stats():
    stats = get_stats()
    stats["is_scraping"] = is_scraping
    return jsonify({"success": True, "stats": stats})

@app.route("/api/trigger-scrape", methods=["POST"])
def api_trigger_scrape():
    global is_scraping
    if is_scraping:
        return jsonify({"success": False, "message": "Scrape already in progress"})
        
    def worker():
        global is_scraping
        is_scraping = True
        try:
            run_all_scrapers()
        finally:
            is_scraping = False
            
    threading.Thread(target=worker, daemon=True).start()
    return jsonify({"success": True, "message": "Job discovery agent started in background"})

if __name__ == "__main__":
    print("🌐 Starting Job Hunter Web Dashboard at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
