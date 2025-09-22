import json
import pytest
from ai_engine import recommender


def test_user_u001(capfd):
    recommender.recommend_for_user("u001")
    out, _ = capfd.readouterr()
    data = json.loads(out.strip())
    assert data["user_id"] == "u001"
    assert "Math" in data["recommended_path"]
    assert "curious" in data["nudge"]


def test_user_u002(capfd):
    recommender.recommend_for_user("u002")
    out, _ = capfd.readouterr()
    data = json.loads(out.strip())
    assert data["user_id"] == "u002"
    assert "Foundations" in data["recommended_path"]
    assert "Focus" in data["nudge"]


def test_user_u003(capfd):
    recommender.recommend_for_user("u003")
    out, _ = capfd.readouterr()
    data = json.loads(out.strip())
    assert data["user_id"] == "u003"
    assert "Science" in data["recommended_path"]
    assert "quiz" in data["nudge"]


def test_user_u004(capfd):
    recommender.recommend_for_user("u004")
    out, _ = capfd.readouterr()
    data = json.loads(out.strip())
    assert data["user_id"] == "u004"
    assert "Confidence" in data["recommended_path"]
    assert "routine" in data["nudge"]


def test_user_u005(capfd):
    recommender.recommend_for_user("u005")
    out, _ = capfd.readouterr()
    data = json.loads(out.strip())
    assert data["user_id"] == "u005"
    assert "Math" in data["recommended_path"]
    assert "quiz" in data["nudge"]


def test_unknown_user(capfd):
    # Call recommender with a non-existent user
    recommender.recommend_for_user("u999")
    out, _ = capfd.readouterr()
    data = json.loads(out.strip())
    assert data["user_id"] == "u999"
    # Should fall back gracefully
    assert "recommended_path" in data
    assert "nudge" in data
