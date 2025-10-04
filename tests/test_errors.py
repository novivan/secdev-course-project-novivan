from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_empty_users():
    r = client.get("/list_users")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 0


def test_adding_user():
    r = client.post("/add_user", params={"user_name": "aaaa"})
    assert r.status_code == 200


def test_empty_features():
    r = client.get("/list_features")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 0


def test_adding_feature():
    r = client.post(
        "/add_feature", params={"feature_title": "bbbb", "feature_description": "cccc"}
    )
    assert r.status_code == 200


def test_empty_votes():
    r = client.get("/list_votes")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 0


def test_adding_vote():
    r = client.post("/add_feature", params={"feature_id": "1", "user_id": "1"})
    assert r.status_code == 200
