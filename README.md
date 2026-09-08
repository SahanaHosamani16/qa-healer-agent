# qa-healer-agent
Self-Healing QA Agent Service
An automated test-healing backend built with FastAPI, Google Cloud Run, Gemini AI, Firestore, and BigQuery. The service intercepts broken test execution payloads, diagnoses failure causes using Generative AI, generates healed CSS/Xpath selectors dynamically, and logs test health telemetry for analytics.
Architecture Overview
                        +---------------------------+
                        |  Test Runner / Framework  |
                        +-------------+-------------+
                                      |
                                      | POST /heal
                                      v
                        +-------------+-------------+
                        |   Google Cloud Run        |
                        |   (FastAPI Backend)       |
                        +------+-------------+------+
                               |             |
            +------------------+             +------------------+
            |                                                   |
            v                                                   v
+-----------+-----------+                           +-----------+-----------+
|   Gemini 3.6 Flash    |                           |  Google Firestore Client  |
|  (Diagnosis & Healer) |                           |  (locator-maps Cache)     |
+-----------------------+                           +-----------+---------------+
                                                                |
                                                                v
                                                    +-----------+---------------+
                                                    |    Google BigQuery        |
                                                    |   (Telemetry & Logs)      |
                                                    +---------------------------+
Architecture Components
API Engine (FastAPI on Cloud Run): Hosts the high-performance async /heal REST endpoint deployed as a containerized, serverless instance.

AI Diagnosis Agent (agents/diagnosis.py): Passes failure payloads (error logs, DOM snippets, failed selectors) to Gemini AI to classify failure root causes.

AI Healing Agent (agents/healer.py): Analyzes the DOM context to generate resilient, updated selectors (e.g., fallback dynamic selectors, test IDs, or structural CSS paths).

Cache Storage (Google Cloud Firestore): Stores updated selector mappings in the locator-maps collection under custom named databases (locator) for instant test lookup.

Analytics Engine (Google BigQuery): Captures test failure metrics and self-healing success rate metrics in qa_telemetry.test_failures.

Repository Structure
qa-healer-agent/
├── agents/
│   ├── diagnosis.py       # AI agent logic for error root cause analysis
│   └── healer.py          # AI agent logic for dynamic selector generation
├── main.py                # FastAPI entrypoint, Firestore connection & BigQuery sync
├── Dockerfile             # Container configuration for Cloud Run
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
