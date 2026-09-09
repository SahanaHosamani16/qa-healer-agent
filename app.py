import streamlit as st
import requests
import json

# Page Configuration
st.set_page_config(
    page_title="Self-Healing QA Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Self-Healing QA Agent Dashboard")
st.caption("AI-Powered Automation Test Failure Diagnosis & Locator Healing")

st.divider()

# Input Form Layout
col1, col2 = st.columns(2)

with col1:
    test_id = st.text_input("Test Case ID", value="TC_LOGIN_001")
    failed_selector = st.text_input("Failed Selector", value="#submit-btn")
    
    error_message = st.text_area(
        "Error Message", 
        value="TimeoutError: element #submit-btn not visible",
        height=100
    )

with col2:
    dom_snippet = st.text_area(
        "DOM Snippet", 
        value='<button class="btn-primary" id="submit-btn-v2" data-testid="checkout-btn">Submit Order</button>',
        height=210
    )

endpoint_url = st.text_input(
    "API Endpoint URL", 
    value="https://self-healing-qa-agent-620727242644.us-central1.run.app/heal"
)

# Trigger Button
if st.button("🚀 Diagnose & Heal Test", type="primary", use_container_width=True):
    payload = {
        "test_id": test_id,
        "error_message": error_message,
        "failed_selector": failed_selector,
        "dom_snippet": dom_snippet
    }
    
    with st.spinner("Analyzing failure with Gemini AI..."):
        try:
            response = requests.post(endpoint_url, json=payload)
            if response.status_code == 200:
                result = response.json()
                
                st.subheader("Results")
                
                # Status Badge
                status = result.get("status", "UNKNOWN")
                if status == "HEALED":
                    st.success(f"Status: **{status}**")
                else:
                    st.error(f"Status: **{status}**")
                
                # Dynamic Output Layout
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    st.markdown("### 🔍 Diagnosis")
                    diag = result.get("diagnosis", {})
                    st.write(f"**Failure Type:** {diag.get('failure_type', 'N/A')}")
                    st.write(f"**Reason:** {diag.get('reason', 'N/A')}")
                    st.write(f"**Fixable by Selector:** `{diag.get('is_fixable_by_selector', False)}`")
                
                with res_col2:
                    st.markdown("### 🔧 Healed Locator")
                    healed = result.get("healed_selector")
                    if healed:
                        st.code(healed, language="css")
                    else:
                        st.warning("No new selector generated.")
                        
            else:
                st.error(f"Error {response.status_code}: {response.text}")
                
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
