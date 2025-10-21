import time
import threading
from database import log_incident

# --- 1. CORRECT THE IMPORT STATEMENT ---
# We are no longer using the old heuristic function.
# We must import our new ML-powered prediction function.
from prioritizer import predict_risk_score_ml

# --- Mock API Integrations (These remain unchanged) ---
def mock_create_jira_ticket(alert, priority="Medium"):
    # ... (no changes here) ...
    print(f"INFO: Creating Jira ticket (Priority: {priority}) for alert '{alert['alert_id']}'...")
    time.sleep(1)
    ticket_id = f"SEC-{int(time.time()) % 1000}"
    print(f"SUCCESS: Created Jira ticket {ticket_id}.")
    return {"status": "success", "ticket_id": ticket_id, "integration": "Jira"}

def mock_send_slack_message(alert, channel="#security-alerts"):
    # ... (no changes here) ...
    print(f"INFO: Sending Slack notification to {channel} for alert '{alert['alert_id']}'...")
    time.sleep(0.5)
    print("SUCCESS: Slack message sent.")
    return {"status": "success", "integration": "Slack"}

def mock_send_email(alert, recipient="soc.manager@example.com"):
    # ... (no changes here) ...
    print(f"INFO: Sending email to {recipient} for alert '{alert['alert_id']}'...")
    time.sleep(0.5)
    print("SUCCESS: Email sent.")
    return {"status": "success", "integration": "Email"}

def mock_isolate_endpoint(alert):
    # ... (no changes here) ...
    print(f"CRITICAL ACTION: Isolating endpoint for alert '{alert['alert_id']}'...")
    time.sleep(1.5)
    print(f"SUCCESS: Endpoint related to '{alert['alert_id']}' has been isolated.")
    return {"status": "success", "integration": "EDR"}


# --- The Core Orchestration Logic (Conditional Playbooks) ---
def run_playbook(alert):
    """
    Executes a conditional playbook based on the alert's ML-predicted risk score.
    """
    # --- 2. UPDATE THE FUNCTION CALL ---
    # Call the new ML function to get the risk score.
    risk_score = predict_risk_score_ml(alert)
    alert['risk_score'] = risk_score
    
    print(f"\n--- Processing Alert: {alert['alert_id']} | ML-Predicted Risk Score: {risk_score} ---")
    
    actions_to_run = []

    # The conditional logic remains the same, as it's based on the 'risk_score' variable.
    if risk_score > 85:
        print("INFO: Triggering CRITICAL Risk Playbook.")
        actions_to_run.extend([
            lambda: mock_isolate_endpoint(alert),
            lambda: mock_create_jira_ticket(alert, priority="Highest"),
            lambda: mock_send_slack_message(alert, channel="#security-critical")
        ])
    elif risk_score > 60:
        print("INFO: Triggering HIGH Risk Playbook.")
        actions_to_run.extend([
            lambda: mock_create_jira_ticket(alert, priority="High"),
            lambda: mock_send_slack_message(alert)
        ])
    elif risk_score > 30:
        print("INFO: Triggering MEDIUM Risk Playbook.")
        actions_to_run.extend([
            lambda: mock_send_email(alert)
        ])
    else:
        print("INFO: Triggering LOW Risk Playbook (Log only).")

    # The concurrent execution logic also remains the same.
    actions_taken = []
    threads = []
    results = [{} for _ in actions_to_run]

    def task_wrapper(func, index):
        results[index] = func()

    for i, action_func in enumerate(actions_to_run):
        thread = threading.Thread(target=task_wrapper, args=(action_func, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    for result in results:
        if result:
            actions_taken.append(f"{result['integration']}: {result.get('ticket_id', result['status'])}")
            
    log_incident(alert, actions_taken)
    
    print(f"--- Finished Processing Alert: {alert['alert_id']} ---")
    return alert