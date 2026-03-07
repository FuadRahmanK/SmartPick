from flask import Flask, request, jsonify
from flask_cors import CORS
from conversation_manager import ConversationManager
import os
import time

app = Flask(__name__)
CORS(app)

managers = {}
SESSION_TIMEOUT = 1800 


def get_manager(session_id):
    now = time.time()

    expired = [
        sid for sid, data in managers.items()
        if now - data["last_used"] > SESSION_TIMEOUT
    ]
    for sid in expired:
        del managers[sid]

    if session_id not in managers:
        managers[session_id] = {
            "manager": ConversationManager("phones.json"),
            "last_used": now
        }

    managers[session_id]["last_used"] = now
    return managers[session_id]["manager"]


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    session_id = data.get("session_id")

    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400

    manager = get_manager(session_id)
    response = manager.handle_message(user_message)
    return jsonify(response)


@app.route("/reset", methods=["POST"])
def reset():
    data = request.json
    session_id = data.get("session_id")

    if session_id in managers:
        del managers[session_id]

    return jsonify({"status": "reset"})


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
