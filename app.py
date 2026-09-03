import streamlit as st
import requests
import json
import asyncio
from google.antigravity import Agent, LocalAgentConfig # Antigravity Agent Runtime

st.set_page_config(page_title="Self-Healing QA Control Center", layout="wide")
st.title("⚡ Self-Healing Enterprise QA Agent Control Center")

CLOUD_RUN_URL = "https://self-healing-qa-agent-xyz-uc.a.run.app/heal"

# Sidebar: Environment & Settings
st.sidebar.header("Configuration")
environment = st.sidebar.selectbox("Target Environment", ["Staging", "QA-Automation-1", "Production-DryRun"])
auto_pr_enabled = st.sidebar.checkbox("Enable Autonomous PR Generation", value=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Simulate Test Execution Failure")
    test_id = st.text_input("Test Case ID", value="TC_CHECKOUT_SUBMIT_01")
    failed_selector = st.text_input("Failed Selector", value="#submit-order-button")
    error_log = st.text_area("Error Stack Trace", value="TimeoutError: Element #submit-order-button not visible within 3000ms")
    dom_snippet = st.text_area("DOM Snippet", value='<button id="btn-submit-v2" class="primary-btn" data-testid="checkout-submit">Complete Order</button>')
    
    trigger_button = st.button("Trigger Self-Healing Workflow", type="primary")

with col2:
    st.subheader("Agent Live Reasoning & Remediation")
    
    if trigger_button:
        with st.spinner("Processing diagnosis via Cloud Run & Gemini..."):
            # 1. Dispatch payload to Cloud Run Healing API
            payload = {
                "test_id": test_id,
                "failed_selector": failed_selector,
                "error_message": error_log,
                "dom_snippet": dom_snippet
            }
            res = requests.post(CLOUD_RUN_URL, json=payload)
            data = res.json()
            
            st.success(f"Status: {data.get('status')}")
            
            # Display Diagnosis
            st.write("**Diagnosis:**")
            st.json(data.get("diagnosis", {}))
            
            # Display New Selector
            healed = data.get("healed_selector")
            if healed:
                st.code(f"Healed Selector: {healed}", language="css")
                
            # 2. Antigravity Agent Streaming reasoning loop for patch application
            st.subheader("Antigravity Agent Patch Execution")
            
            async def run_antigravity_patch():
                config = LocalAgentConfig(
                    system_instructions="You are an Antigravity code patch agent. Create code edits for Playwright tests based on healed locators."
                )
                async with Agent(config) as agent:
                    prompt = f"Write a patch replacing locator {failed_selector} with {healed} in Python Playwright."
                    response = await agent.chat(prompt)
                    
                    # Stream thought traces dynamically
                    async for thought in response.thoughts:
                        st.caption(f"💭 *Thinking:* {thought}")
                    
                    st.markdown(await response.text())

            asyncio.run(run_antigravity_patch())