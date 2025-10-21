# tests/test_vote.py
def test_user_cannot_vote_twice(client):
    register = client.post(
        "/auth/register", data={"username": "voter_user", "password": "securepass123"}
    )
    assert register.status_code == 200, f"Регистрация не удалась: {register.text}"

    login = client.post(
        "/auth/login", data={"username": "voter_user", "password": "securepass123"}
    )
    assert login.status_code == 200
    token = login.json().get("access_token")
    assert token is not None

    client.headers["Authorization"] = f"Bearer {token}"

    feature_response = client.post(
        "/add_feature",
        params={"feature_title": "Dark Mode", "feature_description": "Add dark theme"},
    )
    assert feature_response.status_code == 200

    first_vote = client.post("/features/1/vote")
    assert first_vote.status_code == 200

    second_vote = client.post("/features/1/vote")
    assert second_vote.status_code == 200

    votes = client.get("/list_votes")
    assert votes.status_code == 200
