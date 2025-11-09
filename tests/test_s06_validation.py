from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_reject_short_username():
    r = client.post("/auth/register", data={"username": "ab", "password": "12345"})
    assert r.status_code == 400


def test_register_reject_long_username():
    long_name = "a" * 60
    r = client.post("/auth/register", data={"username": long_name, "password": "12345"})
    assert r.status_code == 400


def test_repeat_vote_does_not_duplicate():
    # register and login
    client.post("/auth/register", data={"username": "voter1", "password": "secure"})
    login = client.post(
        "/auth/login", data={"username": "voter1", "password": "secure"}
    )
    token = login.json().get("access_token")
    assert token is not None
    client.headers["Authorization"] = f"Bearer {token}"
    # add feature
    r = client.post(
        "/add_feature",
        params={"feature_title": "S06 Feature", "feature_description": "desc"},
    )
    assert r.status_code == 200
    # vote twice
    r1 = client.post("/features/1/vote")
    assert r1.status_code == 200
    r2 = client.post("/features/1/vote")
    assert r2.status_code == 200
    # check votes count (should be 1)
    votes = client.get("/list_votes")
    assert votes.status_code == 200
    assert len(votes.json()) == 1
