import pandas as pd
import joblib

try:
    ML_MODEL_PIPELINE = joblib.load('risk_model.joblib')
    print("INFO: Machine Learning risk model loaded successfully.")
except FileNotFoundError:
    ML_MODEL_PIPELINE = None
    print("WARN: 'risk_model.joblib' not found. ML scoring will be disabled.")

def predict_risk_score_ml(alert):
    if not ML_MODEL_PIPELINE:
        return 50 

    alert_df = pd.DataFrame([alert])

    try:
        probability_critical = ML_MODEL_PIPELINE.predict_proba(alert_df)[0][1]
        
        risk_score = int(probability_critical * 100)
        
        return risk_score
    except Exception as e:
        print(f"ERROR: Failed to predict risk score with ML model: {e}")
        return 50 # Return a default medium score on failure

def calculate_risk_score_heuristic(alert):
  
    score = 0
    severity_map = {'Low': 10, 'Medium': 40, 'High': 70}
    score += severity_map.get(alert.get('severity', 'Low'), 10)
    critical_assets = ['Production DB Server', 'Critical File Server', 'Domain Controller']
    if alert.get('asset_type') in critical_assets: score += 25
    high_impact_keywords = ['ransomware', 'sql injection', 'root access']
    description = alert.get('description', '').lower()
    if any(keyword in description for keyword in high_impact_keywords): score += 30
    return min(score, 100)