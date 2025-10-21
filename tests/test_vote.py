def test_user_cannot_vote_twice(client, auth_client):
    # auth_client — клиент с токеном
    auth_client.post(
        "/add_feature", json={"title": "Dark Mode", "desc": "Add dark theme"}
    )
    auth_client.post("/features/1/vote")
    response = auth_client.post("/features/1/vote")
    assert response.status_code == 200
