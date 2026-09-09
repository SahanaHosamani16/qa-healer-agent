import json
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import firestore, bigquery
from agents.diagnosis import diagnose_failure
from agents.healer import suggest_healed_selector

app = FastAPI(title="Self-Healing QA Agent Service")

# Fix: Custom database IDs must be 'locator', not '(locator)'
DATABASE_ID = os.getenv("FIRESTORE_DATABASE", "locator")
db = firestore.Client(database=DATABASE_ID)
bq_client = bigquery.Client()

class FailurePayload(BaseModel):
    test_id: str
    error_message: str
    failed_selector: str
    dom_snippet: str

@app.post("/heal")
async def heal_test(payload: FailurePayload):
    # 1. Run Diagnosis
    diagnosis_raw = diagnose_failure(
        payload.error_message, payload.dom_snippet, payload.failed_selector
    )
    diagnosis = json.loads(diagnosis_raw)
    
    healed_selector = None
    status = "FAILED"
    
    # 2. Heal if selector is the issue
    if diagnosis.get("is_fixable_by_selector"):
        healing_raw = suggest_healed_selector(payload.failed_selector, payload.dom_snippet)
        healing_data = json.loads(healing_raw)
        healed_selector = healing_data.get("new_selector")
        status = "HEALED"
        
        # Update Firestore locator mapping cache
        db.collection("locator-maps").document(payload.test_id).set({
            "original_selector": payload.failed_selector,
            "active_selector": healed_selector,
            "updated_at": firestore.SERVER_TIMESTAMP
        }, merge=True)

    # 3. Log Telemetry to BigQuery
    table_id = f"{bq_client.project}.qa_telemetry.test_failures"
    rows_to_insert = [{
        "test_id": payload.test_id,
        "timestamp": datetime.utcnow().isoformat(),
        "error_message": payload.error_message[:500],
        "failed_selector": payload.failed_selector,
        "healed_selector": healed_selector,
        "status": status
    }]
    bq_client.insert_rows_json(table_id, rows_to_insert)

    return {
        "status": status,
        "diagnosis": diagnosis,
        "healed_selector": healed_selector
    }
