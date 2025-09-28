from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_adding_user():
    r = client.post("/add_user", params={"user_name": "aaaa"})
    assert r.status_code == 200


def test_empty_users():
    r = client.get("/list_users")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 0
