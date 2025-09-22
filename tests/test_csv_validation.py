import csv
import os
import pytest

# Expected keywords based on tests
EXPECTED = {
    "u001": {"path": "Math", "nudge": "curious"},
    "u002": {"path": "Foundations", "nudge": "Focus"},
    "u003": {"path": "Science", "nudge": "quiz"},
    "u004": {"path": "Confidence", "nudge": "routine"},
    "u005": {"path": "Math", "nudge": "quiz"},
}

DATA_FILE = os.path.join("data", "recommendations.csv")

@pytest.mark.parametrize("user_id, expected", EXPECTED.items())
def test_csv_consistency(user_id, expected):
    with open(DATA_FILE, newline="") as f:
        reader = csv.DictReader(f)
        found = None
        for row in reader:
            if row["user_id"] == user_id:
                found = row
                break
        assert found, f"User {user_id} not found in CSV"
        assert expected["path"] in found["recommended_path"], \
            f"{user_id}: expected path containing '{expected['path']}', got '{found['recommended_path']}'"
        assert expected["nudge"].lower() in found["nudge"].lower(), \
            f"{user_id}: expected nudge containing '{expected['nudge']}', got '{found['nudge']}'"
