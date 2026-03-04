import json
import os
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "mixtral-8x7b-32768"


def call_groq(prompt, temperature=0.3):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a precise assistant. Follow instructions strictly."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


def normalize_user_input(text):
    prompt = f"""
Correct spelling mistakes only.
Do NOT change meaning.
Return only corrected sentence.

Text:
{text}
"""
    ai_output = call_groq(prompt, temperature=0)
    return ai_output if ai_output else text


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
    ai_output = call_groq(prompt)

    if not ai_output:
        return None

    try:
        start = ai_output.find("{")
        end = ai_output.rfind("}") + 1
        return json.loads(ai_output[start:end])
    except Exception:
        return None


def infer_rating_with_ai(user_text, feature_name):
    prompt = f"""
User answered about importance of {feature_name}.
Return ONLY a number from 1 to 5.

Text:
{user_text}
"""
    ai_output = call_groq(prompt, temperature=0)

    if ai_output:
        for ch in ai_output:
            if ch in ["1", "2", "3", "4", "5"]:
                return int(ch)

    return None