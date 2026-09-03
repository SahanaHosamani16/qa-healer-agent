import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def suggest_healed_selector(failed_selector: str, dom_snippet: str) -> str:
    prompt = f"""
    A Playwright/Selenium test failed because the locator '{failed_selector}' was not found.
    
    Inspect this DOM snippet and find the intended target element:
    ```html
    {dom_snippet}
    ```
    
    Return a JSON object with:
    1. "new_selector": The most resilient CSS selector or XPath (prefer robust data-testid or aria attributes over brittle class chains).
    2. "confidence": High, Medium, or Low.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )
    return response.text