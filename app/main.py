# app/main.py
import os
import csv
import logging
from flask import Flask, request, jsonify

# Import recommender from package ai_engine
from ai_engine.recommender import recommend_for_user_row

app = Flask(__name__)

# Path to data/mock_users.csv (project_root/data/mock_users.csv)
DATA_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mock_users.csv")

def find_user_row(user_id: str):
    """Return CSV row dict for a given user_id, or None if not found."""
    try:
        with open(DATA_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r.get("user_id") == user_id:
                    return r
    except FileNotFoundError:
        app.logger.error("Data file not found at %s", DATA_CSV)
    return None

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "ok",
        "message": "EmpowerEd USSD simulator. POST JSON to /ussd with {session_id, user_id, input}"
    }), 200

@app.route("/ussd", methods=["POST"])
def ussd():
    # Accept JSON body
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id", "unknown")
    user_id = (data.get("user_id") or "").strip()
    session_input = str(data.get("input") or "").strip()

    if not user_id:
        return jsonify({
            "session_id": session_id,
            "response": "Welcome to EmpowerEd. Please provide your user_id (e.g., u001)."
        }), 200

    user_row = find_user_row(user_id)
    if not user_row:
        return jsonify({
            "session_id": session_id,
            "response": "User not found. Try u001, u002, u003, u004, u005."
        }), 200

    # Menu when input is empty or "0"
    if session_input == "" or session_input == "0":
        menu = (
            "Welcome back! Choose:\n"
            "1) My learning path\n"
            "2) Today's nudge\n"
            "3) Quick lesson\n"
            "0) Exit"
        )
        return jsonify({"session_id": session_id, "response": menu}), 200

    # Handle choices
    if session_input == "1":
        rec = recommend_for_user_row(user_row)
        return jsonify({
            "session_id": session_id,
            "response": f"Recommended path: {rec['recommended_path']}"
        }), 200

    if session_input == "2":
        rec = recommend_for_user_row(user_row)
        return jsonify({
            "session_id": session_id,
            "response": f"Nudge: {rec['nudge']}"
        }), 200

    if session_input == "3":
        return jsonify({
            "session_id": session_id,
            "response": "Micro-lesson: Read 5 minutes on a topic you like. Tip: write one example."
        }), 200

    return jsonify({
        "session_id": session_id,
        "response": "Invalid input. Reply with 1, 2, 3 or 0."
    }), 200

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Use a conventional Flask port 5000 so curls below work
    app.run(host="127.0.0.1", port=5000, debug=True)
