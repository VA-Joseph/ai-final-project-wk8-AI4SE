from ai_engine.recommender import recommend_for_user_row

def test_recommender_high_curiosity():
    row = {"user_id":"t1","age":"14","gender":"F","attendance_rate":"0.9","curiosity_score":"9","consistency_score":"8","preferred_subject":"math"}
    res = recommend_for_user_row(row)
    assert "Exploratory" in res["recommended_path"]

def test_recommender_low_attendance():
    row = {"user_id":"t2","age":"15","gender":"M","attendance_rate":"0.2","curiosity_score":"2","consistency_score":"1","preferred_subject":"none"}
    res = recommend_for_user_row(row)
    assert "Re-engagement" in res["recommended_path"]
