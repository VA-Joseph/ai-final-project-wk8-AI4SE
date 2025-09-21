"""
Simple rule-based recommender for EmpowerEd.
Given a user's behavioral scores, recommend a learning path and a short nudge.
"""

import csv
from typing import Dict, Any

def load_user(user_row: Dict[str, str]) -> Dict[str, Any]:
    """Convert CSV row to typed dict"""
    return {
        "user_id": user_row["user_id"],
        "age": int(user_row["age"]),
        "gender": user_row["gender"],
        "attendance_rate": float(user_row["attendance_rate"]),
        "curiosity": int(user_row["curiosity_score"]),
        "consistency": int(user_row["consistency_score"]),
        "preferred_subject": user_row.get("preferred_subject") or "general"
    }

def score_to_path(user: Dict[str, Any]) -> Dict[str, str]:
    """Very simple logic mapping scores to a path and a nudge message."""
    curiosity = user["curiosity"]
    consistency = user["consistency"]
    attendance = user["attendance_rate"]

    # default
    path = "General Foundations"
    nudge = "Keep going — small daily practice helps!"

    if curiosity >= 8 and consistency >= 6:
        path = f"Exploratory: Deepen in {user['preferred_subject'].title()}"
        nudge = "You're curious & consistent — try a challenge project!"
    elif curiosity >= 6:
        path = f"Guided: Explore {user['preferred_subject'].title()}"
        nudge = "Explore short lessons and try a mini-quiz each day."
    elif consistency >= 7:
        path = "Practice-Focused: Strengthen fundamentals"
        nudge = "Great consistency — keep a steady study schedule."
    elif attendance < 0.5 or consistency < 3:
        path = "Re-engagement: Short motivation + micro-lessons"
        nudge = "Start with 5-minute daily lessons and celebrate small wins."
    else:
        path = "Foundations: Core skills"
        nudge = "Focus on core topics for 10 mins a day."

    # If attendance very low, emphasise re-engagement
    if attendance < 0.5:
        path = "Re-engagement: Attendance & Confidence Boost"
        nudge = "Let's rebuild routine — 3 short lessons this week."

    return {"path": path, "nudge": nudge}

def recommend_for_user_row(row: Dict[str, str]) -> Dict[str, Any]:
    user = load_user(row)
    rec = score_to_path(user)
    result = {
        "user_id": user["user_id"],
        "recommended_path": rec["path"],
        "nudge": rec["nudge"]
    }
    return result

def recommend_from_csv(path_to_csv: str):
    """Yield recommendations for all users in a CSV file."""
    with open(path_to_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield recommend_for_user_row(row)

# Quick CLI usage
if __name__ == "__main__":
    import json
    for r in recommend_from_csv("data/mock_users.csv"):
        print(json.dumps(r, ensure_ascii=False))
