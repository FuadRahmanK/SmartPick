import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


def generate_ai_response(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "num_predict": 150
                }
            },
            timeout=60
        )

        result = response.json()
        return result.get("response", "").strip()

    except Exception:
        return fallback_response(prompt)


def generate_recommendation_text(phone_list, state):
    if not phone_list:
        return "I couldn't find a suitable match."

    summary = "\n".join([
        f"{i+1}. {p['name']} (₹{p['price']}) - Score: {p['final_score']}"
        for i, p in enumerate(phone_list)
    ])

    prompt = f"""
You are a professional smartphone advisor.

User preferences:
Budget: {state.get("budget")}
OS: {state.get("os_preference")}
Feature importance: {json.dumps(state.get("clarified_features"))}

Top ranked phones:
{summary}

Explain naturally why the FIRST phone is the best match.
Keep it under 120 words.
"""

    return generate_ai_response(prompt)


def fallback_response(prompt):
    return "Could you tell me a bit more about your preferences?"