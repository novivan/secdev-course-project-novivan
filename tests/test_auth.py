def test_login_success(client):
    client.post("/auth/register", data={"username": "test", "password": "123"})
    response = client.post("/auth/login", data={"username": "test", "password": "123"})
    assert response.status_code == 200
    assert "access_token" in response.json()