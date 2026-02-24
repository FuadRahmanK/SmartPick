import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


# ----------------------------------------------------
# Safe Ollama Call
# ----------------------------------------------------
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


# ----------------------------------------------------
# Normalize User Input
# ----------------------------------------------------
def normalize_user_input(text):
    prompt = f"""
Correct spelling mistakes and rewrite clearly.
Do NOT change meaning.
Return only the corrected sentence.

Text:
{text}
"""
    ai_output = call_ollama(prompt)
    return ai_output if ai_output else text


# ----------------------------------------------------
# AI Structured Extraction
# ----------------------------------------------------
def extract_structured_info_with_ai(user_text):

    prompt = f"""
Extract structured information from the user's message.

Return ONLY valid JSON in this format:

{{
  "budget": number or null,
  "os_preference": "Android", "iOS", "Any", or null,
  "feature_priority": "camera", "battery", "performance", "display", "software", or null
}}

User Message:
{user_text}
"""

    ai_output = call_ollama(prompt)

    if not ai_output:
        return None

    try:
        start = ai_output.find("{")
        end = ai_output.rfind("}") + 1
        json_text = ai_output[start:end]
        return json.loads(json_text)
    except:
        return None


# ----------------------------------------------------
# AI Behavioral Rating
# ----------------------------------------------------
def infer_rating_with_ai(user_text, feature_name):

    prompt = f"""
A user answered a question about their {feature_name} usage.

Return ONLY a number from 1 to 5.

1 = Very Low Importance
5 = Very High Importance

User Response:
{user_text}
"""

    ai_output = call_ollama(prompt)

    if ai_output:
        for char in ai_output:
            if char in ["1", "2", "3", "4", "5"]:
                return int(char)

    return None


# ----------------------------------------------------
# Recommendation Explanation
# ----------------------------------------------------
def generate_recommendation_text(recommendations, state):

    if not recommendations:
        return "No suitable phones found within your criteria."

    top_phone = recommendations[0]

    base = f"""
The {top_phone['name']} is the best match for your preferences.
It fits your budget and aligns strongly with your priorities.
Overall score: {top_phone['final_score']}.
"""

    prompt = f"""
Explain professionally why this phone is best.

Phone: {top_phone['name']}
Score: {top_phone['final_score']}
User Preferences: {state}
"""

    ai_output = call_ollama(prompt)

    return ai_output if ai_output else base.strip()