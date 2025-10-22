# AI-Powered SOAR Engine
*A Modern Security Orchestration, Automation, and Response (SOAR) Platform Prototype*

### Overview
The **AI-Powered SOAR Engine** is a next-generation cybersecurity automation platform designed to tackle two critical challenges in modern Security Operations Centers (SOCs): **alert fatigue** and **slow incident response times**. By integrating **Machine Learning** into traditional SOAR workflows, this system intelligently prioritizes alerts and triggers **context-aware, automated responses**, enabling analysts to focus on what truly matters.

---

###  Key Highlights
-  **AI-Driven Risk Prioritization** – Uses a trained `RandomForestClassifier` to assign precise risk scores, distinguishing genuine threats from noise.
-  **Dynamic Playbook Automation** – Executes tailored response workflows based on predicted alert severity, enabling adaptive orchestration.
-  **Real-Time SOC Integration** – Pushes formatted incident alerts directly to **Slack** channels for instant team awareness.
-  **Interactive Analytics Dashboard** – Built with Flask and Chart.js, the dashboard delivers live KPIs, risk trends, and an intuitive incident queue.
-  **Persistent Incident Logging** – Maintains a detailed SQLite-based audit trail of alerts and actions.

---

###  Technology Stack
*   **Backend:** Python · Flask · Pandas · Scikit-learn · Joblib
*   **Frontend:** HTML5 · CSS3 · JavaScript · Chart.js
*   **Database:** SQLite
*   **Integration:** Slack Webhooks

---

###  Getting Started

#### Prerequisites
- Python **3.8+**
- Git
- Pip (Python package manager)

#### Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/SanayKrishna/Ai-Powered-Soar-Engine.git
    cd Ai-Powered-Soar-Engine
    ```

2.  **Create and activate a virtual environment**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # For macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies from `requirements.txt`**  
    *(Note: If `requirements.txt` doesn't exist yet, create it by running `pip freeze > requirements.txt`)*
    ```bash
    pip install -r requirements.txt
    ```

#### Data & Model Generation

1.  **Generate synthetic data for training**
    ```bash
    python generate_data.py
    ```

2.  **Train the AI model**
    ```bash
    python train_model.py
    ```
    *This creates the `risk_model.joblib` file used by the application.*

#### Running the Application

1.  **Add your Slack Webhook URL**  
    Open `orchestrator.py` and replace the placeholder `YOUR_SLACK_WEBHOOK_URL_HERE` with your actual URL.

2.  **Launch the SOAR Engine**
    ```bash
    python app.py
    ```
    Visit **http://127.0.0.1:5001** in your browser to view the dashboard.

---

###  Project Workflow
-  **Alert Ingestion** – Simulates data from sources like EDRs, Firewalls, and CSPM tools.
-  **AI Prioritization** – Assigns a risk score (1–100) for each alert using the trained model.
-  **Automated Orchestration** – Conditional playbooks determine the appropriate response workflow.
-  **Response Execution** – Executes actions such as ticket creation, Slack alerts, or endpoint isolation.
-  **Persistent Logging** – All incidents and actions are recorded in SQLite for a full audit trail.
-  **Visualization** – Real-time results are displayed on the interactive dashboard.

---

### 📈 Future Enhancements
- 🔐 **Configuration Management** – Store sensitive data in a secure `config.ini` or `.env` file.
- 🧩 **Threat Intelligence Enrichment** – Integrate APIs like VirusTotal for IOC lookups.
- 👤 **User Authentication** – Add secure login and role-based dashboard access.
- ☁️ **Cloud Integration** – Extend playbooks for AWS, Azure, and other cloud service providers.
