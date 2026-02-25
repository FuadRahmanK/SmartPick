import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


# ---------------- SAFE OLLAMA CALL ----------------
def call_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=2
        )
        if response.status_code == 200:
            return response.json().get("response", "").strip()
    except:
        pass
    return None


# ---------------- NORMALIZE INPUT ----------------
def normalize_user_input(text):
    prompt = f"""
Correct spelling mistakes only.
Do NOT change meaning.
Return only corrected sentence.

Text:
{text}
"""
    ai_output = call_ollama(prompt)
    return ai_output if ai_output else text


# ---------------- AI STRUCTURED EXTRACTION ----------------
def extract_structured_info_with_ai(user_text):

    prompt = f"""
Extract structured info and return ONLY JSON:

{{
  "os_preference": "Android", "iOS", "Any", or null,
  "feature_priority": "camera", "battery", "performance", "display", "software", or null
}}

User:
{user_text}
"""

    ai_output = call_ollama(prompt)

    if not ai_output:
        return None

    try:
        start = ai_output.find("{")
        end = ai_output.rfind("}") + 1
        return json.loads(ai_output[start:end])
    except:
        return None


# ---------------- AI RATING ----------------
def infer_rating_with_ai(user_text, feature_name):

    prompt = f"""
User answered about importance of {feature_name}.
Return ONLY a number from 1 to 5.

Text:
{user_text}
"""

    ai_output = call_ollama(prompt)

    if ai_output:
        for ch in ai_output:
            if ch in ["1", "2", "3", "4", "5"]:
                return int(ch)

    return None


# ---------------- EXPLANATION ----------------
def generate_recommendation_text(recommendations, state):

    if not recommendations:
        return "No suitable phones found within your criteria."

    top = recommendations[0]

    base = f"""
The {top['name']} is the best match for your needs.
It aligns strongly with your priorities and budget.
Final score: {top['final_score']}.
"""

    prompt = f"""
Explain briefly why this phone is best.

Phone: {top['name']}
Score: {top['final_score']}
Preferences: {state}
"""

    ai_output = call_ollama(prompt)
    return ai_output if ai_output else base.strip()