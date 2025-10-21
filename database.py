import sqlite3
import json
from datetime import datetime

DB_FILE = 'data/soar.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        processed_at TEXT NOT NULL,
        alert_id TEXT NOT NULL UNIQUE,
        source TEXT,
        severity TEXT,
        description TEXT,
        asset_type TEXT,
        risk_score INTEGER,
        status TEXT,
        actions_taken TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    print("INFO: Database initialized successfully.")

def log_incident(alert, actions):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO incidents (processed_at, alert_id, source, severity, description, asset_type, risk_score, status, actions_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.utcnow().isoformat(),
            alert.get('alert_id'),
            alert.get('source'),
            alert.get('severity'),
            alert.get('description'),
            alert.get('asset_type'),
            alert.get('risk_score'),
            'Resolved',
            json.dumps(actions) # Store list of actions as a JSON string
        ))
        conn.commit()
        print(f"SUCCESS: Incident for alert '{alert.get('alert_id')}' logged to database.")
    except sqlite3.IntegrityError:
        print(f"WARN: Incident for alert '{alert.get('alert_id')}' already exists in the database. Skipping.")
    except Exception as e:
        print(f"ERROR: Failed to log incident to database: {e}")
    finally:
        conn.close()

def get_all_incidents():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    incidents = cursor.execute('SELECT * FROM incidents ORDER BY processed_at DESC').fetchall()
    conn.close()
    
    results = []
    for incident in incidents:
        row = dict(incident)
        row['actions_taken'] = json.loads(row['actions_taken'])
        results.append(row)
        
    return results