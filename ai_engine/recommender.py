import csv
import json
import os

# Path to your CSV file
DATA_FILE = os.path.join("data", "recommendations.csv")


def recommend_for_user(user_id: str):
    """Return recommendation for a given user_id, or None if not found."""
    try:
        with open(DATA_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["user_id"] == user_id:
                    result = {
                        "user_id": row["user_id"],
                        "recommended_path": row.get("recommended_path"),
                        "nudge": row.get("nudge"),
                    }
                    print(json.dumps(result))  # Print JSON for pytest
                    return result
    except FileNotFoundError:
        # If the CSV file is missing
        result = {"user_id": user_id, "recommended_path": None, "nudge": None}
        print(json.dumps(result))
        return result

    # User not found in CSV
    result = {"user_id": user_id, "recommended_path": None, "nudge": None}
    print(json.dumps(result))
    return result


if __name__ == "__main__":
    # Quick manual test
    sample_user = "u001"
    recommend_for_user(sample_user)
