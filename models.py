import sqlite3
import datetime
from config import DB_PATH

SENIOR_KEYWORDS_SQL = [
    "%senior%", "%sr.%", "%sr %", "%lead%", "%manager%", "%architect%", "%principal%",
    "%staff%", "%head of%", "%director%", "%vp%", "%executive%", "%expert%", "%tech lead%", "%team lead%"
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Jobs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT,
        location_priority INTEGER DEFAULT 99,
        job_type TEXT DEFAULT 'Full Time', -- 'Full Time' or 'Internship'
        platform TEXT NOT NULL,
        url TEXT UNIQUE NOT NULL,
        description TEXT,
        salary TEXT,
        posted_date TEXT,
        discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        match_score INTEGER DEFAULT 0,
        status TEXT DEFAULT 'new', -- 'new', 'applied', 'saved', 'ignored'
        is_duplicate INTEGER DEFAULT 0
    )
    ''')
    
    # Scrape Logs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scrape_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,
        jobs_found INTEGER DEFAULT 0,
        new_jobs INTEGER DEFAULT 0,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    purge_senior_jobs()

def purge_senior_jobs():
    """Remove any senior or experienced roles from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for kw in SENIOR_KEYWORDS_SQL:
        cursor.execute('DELETE FROM jobs WHERE LOWER(title) LIKE ?', (kw,))
        
    conn.commit()
    conn.close()

def save_job(job_data):
    """Save or ignore existing job based on URL"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO jobs (id, title, company, location, location_priority, job_type, platform, url, description, salary, posted_date, match_score, status)
        VALUES (:id, :title, :company, :location, :location_priority, :job_type, :platform, :url, :description, :salary, :posted_date, :match_score, 'new')
        ''', job_data)
        conn.commit()
        inserted = True
    except sqlite3.IntegrityError:
        inserted = False
        
    conn.close()
    return inserted

def update_job_status(job_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE jobs SET status = ? WHERE id = ?', (new_status, job_id))
    conn.commit()
    conn.close()

def get_jobs(job_type=None, status=None, min_score=0, limit=150):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = 'SELECT * FROM jobs WHERE match_score >= ?'
    params = [min_score]
    
    if job_type:
        query += ' AND job_type = ?'
        params.append(job_type)
        
    if status:
        query += ' AND status = ?'
        params.append(status)
    else:
        query += ' AND status != "ignored"'
        
    # Sort by location priority (1=Nashik, 2=Pune, 3=Mumbai, 4=Remote, 5=India), then match_score desc, then discovered_at desc
    query += ' ORDER BY location_priority ASC, match_score DESC, discovered_at DESC LIMIT ?'
    params.append(limit)
    
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM jobs')
    total_found = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM jobs WHERE status = "new"')
    new_jobs = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM jobs WHERE status = "applied"')
    applied_jobs = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM jobs WHERE job_type = "Internship"')
    internships = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM jobs WHERE job_type = "Full Time"')
    full_times = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total_found": total_found,
        "new_jobs": new_jobs,
        "applied_jobs": applied_jobs,
        "internships": internships,
        "full_times": full_times
    }

if __name__ == "__main__":
    init_db()
    print("Database initialized & purged of senior jobs.")
