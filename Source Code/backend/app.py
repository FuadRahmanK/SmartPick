from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os

from conversation_manager import ConversationManager

app = Flask(
    __name__,
    static_folder="../frontend/build",
    static_url_path="/"
)

app.secret_key = "change_this_secret_key"
CORS(app)


# ----------------------------------------------------
# Helper: Initialize or Restore State
# ----------------------------------------------------
def get_conversation_manager():
    manager = ConversationManager("phones.json")

    # Restore state if exists
    if "state" in session:
        manager.state = session["state"]

    return manager


def save_state(manager):
    session["state"] = manager.state


# ----------------------------------------------------
# API Endpoint
# ----------------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    manager = get_conversation_manager()

    response = manager.handle_message(user_message)

    # Save updated state
    save_state(manager)

    if response["type"] == "question":
        return jsonify({
            "type": "question",
            "message": response["message"]
        })

    elif response["type"] == "recommendation":
        formatted_results = []

        for phone in response["data"]:
            formatted_results.append({
                "name": phone["name"],
                "brand": phone["brand"],
                "price": phone["price"],
                "score": phone["final_score"],
                "processor": phone["processor_name"],
                "explanation": phone["explanation"]
            })

        return jsonify({
            "type": "recommendation",
            "results": formatted_results
        })


# ----------------------------------------------------
# Serve React Frontend
# ----------------------------------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


# ----------------------------------------------------
# Run Server
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)