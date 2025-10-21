import pandas as pd
import random
import json

NUM_SAMPLES = 5000
SOURCES = ['Firewall', 'EDR', 'CSPM', 'IDS', 'PhishingFilter']
ASSET_TYPES = ['Production DB Server', 'Critical File Server', 'Domain Controller', 'Standard Workstation', 'Dev Server', 'Cloud Storage']
USER_ROLES = ['Administrator', 'Finance', 'DevOps', 'Marketing', 'Sales', 'N/A']
HIGH_IMPACT_KEYWORDS = ['ransomware', 'sql injection', 'root access', 'data exfiltration', 'domain admin']
LOW_IMPACT_KEYWORDS = ['public access', 'unusual login', 'policy violation', 'port scan', 'failed login']

def generate_alert():
    source = random.choice(SOURCES)
    asset_type = random.choice(ASSET_TYPES)
    user_role = random.choice(USER_ROLES)
    
    is_critical = 0
    description_parts = []

    if random.random() < 0.5:
        if asset_type in ['Production DB Server', 'Critical File Server', 'Domain Controller']:
            is_critical = 1
            description_parts.append(random.choice(HIGH_IMPACT_KEYWORDS))
        if user_role == 'Administrator':
            is_critical = 1
            description_parts.append("on admin account")
        
        description_parts.append(random.choice(LOW_IMPACT_KEYWORDS))
    else:
        description_parts.append(random.choice(LOW_IMPACT_KEYWORDS))

    description_parts.append(f"from IP 10.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
    
    description = ' '.join(description_parts)

    return {
        'source': source,
        'asset_type': asset_type,
        'user_role': user_role,
        'description': description,
        'is_critical': is_critical 
    }

if __name__ == "__main__":
    print(f"Generating {NUM_SAMPLES} mock alerts for training...")
    alerts = [generate_alert() for _ in range(NUM_SAMPLES)]
    
    df = pd.DataFrame(alerts)
    
    output_path = 'data/training_alerts.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Data generation complete. Saved to '{output_path}'")
    print("\nSample of generated data:")
    print(df.head())
    print(f"\nDistribution of critical alerts:\n{df['is_critical'].value_counts(normalize=True)}")