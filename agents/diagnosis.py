import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def diagnose_failure(error_log: str, dom_snippet: str, failed_selector: str) -> dict:
    prompt = f"""
    You are an expert QA Automation Engineer. Analyze the following UI test failure.
    
    Failed Selector: {failed_selector}
    Error Log: {error_log}
    Page DOM Snippet:
    ```html
    {dom_snippet}
    ```
    
    Identify if the failure was caused by a changed DOM element/attribute or a timing/timeout issue.
    Provide your analysis as a structured JSON object with keys: "failure_type", "reason", "is_fixable_by_selector".
    """
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )
    return response.text
