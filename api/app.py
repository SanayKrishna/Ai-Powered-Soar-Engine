from flask import Flask, render_template, jsonify
import pandas as pd
import json
import sqlite3
from orchestrator import run_playbook
from database import init_db, get_all_incidents, DB_FILE

app = Flask(__name__, template_folder='../templates', static_folder='../static')


SIMULATION_HAS_RUN = False

def run_full_simulation():
    global SIMULATION_HAS_RUN
    if SIMULATION_HAS_RUN:
        return
    
    print("--- Initializing Database ---")
    init_db()

    print("--- Starting Full SOAR Simulation ---")
    try:
        with open('data/alerts.json', 'r') as f:
            alerts_to_process = json.load(f)
        
        for alert in alerts_to_process:
            run_playbook(alert)

        print("\n--- SOAR Simulation Finished ---")
        SIMULATION_HAS_RUN = True

    except Exception as e:
        print(f"ERROR during simulation: {e}")

@app.route('/')
def dashboard():
    run_full_simulation()
    
    incidents = get_all_incidents()
    incidents_sorted = sorted(incidents, key=lambda x: x['risk_score'], reverse=True)
    
    return render_template('index.html', incidents=incidents_sorted)

@app.route('/api/trends')
def trends_data():
    conn = sqlite3.connect(DB_FILE)
    
    source_df = pd.read_sql_query('SELECT source, COUNT(*) as count FROM incidents GROUP BY source', conn)
    
    severity_df = pd.read_sql_query('SELECT severity, COUNT(*) as count FROM incidents GROUP BY severity', conn)
    
    conn.close()
    
    trends = {
        'by_source': source_df.to_dict(orient='records'),
        'by_severity': severity_df.to_dict(orient='records')
    }
    return jsonify(trends)

if __name__ == '__main__':
    app.run(debug=True, port=5001)