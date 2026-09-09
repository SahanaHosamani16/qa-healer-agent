# qa-healer-agent
Self-Healing QA Agent Service
An automated test-healing backend built with FastAPI, Google Cloud Run, Gemini AI, Firestore, and BigQuery. The service intercepts broken test execution payloads, diagnoses failure causes using Generative AI, generates healed CSS/Xpath selectors dynamically, and logs test health telemetry for analytics.

Architecture Overview
<img width="4032" height="1847" alt="image" src="https://github.com/user-attachments/assets/2772ef54-d65f-4485-b3af-f7d830a6b9fb" />
                      

Architecture Components
*Web UI (`app.py`):** Interactive Streamlit dashboard for real-time manual testing, failure diagnosis visualization, and locator updates.
* **API Engine (`main.py`):** High-performance FastAPI REST service deployed on Cloud Run handling `/heal` endpoints.
* **AI Diagnosis Agent (`agents/diagnosis.py`):** Leverages Gemini AI to analyze failure logs, DOM snippets, and selector context to identify root causes.
* **AI Healing Agent (`agents/healer.py`):** Evaluates updated DOM structures to construct dynamic, resilient replacement locators.
* **Cache Engine (Google Cloud Firestore):** Maintains active selector maps in named databases (`locator`) under the `locator-maps` collection.
* **Analytics Engine (Google BigQuery):** Captures test execution failure logs and healing status in `qa_telemetry.test_failures`.

qa-healer-agent/
├── agents/
│   ├── diagnosis.py       # AI agent logic for error root cause analysis
│   └── healer.py          # AI agent logic for dynamic selector generation
├── app.py                 # Streamlit Web UI dashboard
├── main.py                # FastAPI entrypoint, Firestore connection & BigQuery sync
├── Dockerfile             # Container setup for FastAPI backend
├── Dockerfile.ui          # Container setup for Streamlit Web UI
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation

API ReferencePOST /healAnalyzes test failures, evaluates fixability, generates replacement selectors, and updates cache/telemetry.Request BodyJSON{
  "test_id": "TC_LOGIN_001",
  "error_message": "TimeoutError: element #submit-btn not visible",
  "failed_selector": "#submit-btn",
  "dom_snippet": "<button class=\"btn-primary\" id=\"submit-btn-v2\" data-testid=\"checkout-btn\">Submit Order</button>"
}
Response BodyJSON{
  "status": "HEALED",
  "diagnosis": {
    "failure_type": "DOM Element Attribute Change",
    "reason": "The ID of the button element changed from 'submit-btn' to 'submit-btn-v2'.",
    "is_fixable_by_selector": true
  },
  "healed_selector": "[data-testid=\"checkout-btn\"]"
}
Variable	Description	Example / DefaultGEMINI_API_KEY	Google Gemini API Key	AIzaSy...
GCP_PROJECT	Google Cloud Project ID	ABC-lang-DEF-0914005407
FIRESTORE_DATABASE	Firestore Database Identifier	locator
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets GEMINI_API_KEY=GEMINI_API_KEY:latest \
  --set-env-vars FIRESTORE_DATABASE=locator
2. Deploy Streamlit Web UI to Cloud RunBashgcloud run deploy qa-agent-ui \
  --source . \
  --dockerfile Dockerfile.ui \
  --region us-central1 \
  --allow-unauthenticated
