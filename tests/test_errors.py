from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rfc7807_format_for_unauthorized():
    """Проверяем, что 401 возвращается в формате RFC 7807"""
    response = client.get("/list_users")
    assert response.status_code == 401
    data = response.json()
    assert "correlation_id" in data
    assert data["type"] == "about:blank"
    assert data["status"] == 401
    assert data["title"] == "http_error"


def test_protected_routes_require_auth():
    """Проверяем, что все защищённые роуты требуют авторизации"""
    protected_routes = [
        ("GET", "/list_users"),
        ("GET", "/list_features"),
        ("GET", "/list_votes"),
        ("POST", "/add_user"),
        ("POST", "/add_feature"),
        ("POST", "/add_vote"),
    ]

    for method, url in protected_routes:
        if method == "GET":
            response = client.get(url)
        elif method == "POST":
            response = client.post(url)
        assert response.status_code == 401, f"{method} {url} должен требовать авторизацию"


def test_authenticated_requests_work():
    """Регистрация → логин → вызов защищённых роутов"""
    # 1. Регистрация
    r = client.post("/auth/register", data={"username": "testuser", "password": "123456"})
    assert r.status_code in [200, 201], f"Регистрация не удалась: {r.text}"

    # 2. Логин
    r = client.post("/auth/login", data={"username": "testuser", "password": "123456"})
    assert r.status_code == 200
    token = r.json().get("access_token")
    assert token is not None

    # 3. Устанавливаем заголовок авторизации
    client.headers["Authorization"] = f"Bearer {token}"

    # 4. Проверяем пустые списки
    r = client.get("/list_users")
    assert r.status_code == 200
    assert len(r.json()) > 0  # должен быть хотя бы testuser

    r = client.get("/list_features")
    assert r.status_code == 200
    assert len(r.json()) == 0

    r = client.get("/list_votes")
    assert r.status_code == 200
    assert len(r.json()) == 0

    # 5. Добавляем фичу
    r = client.post("/add_feature", params={"feature_title": "Dark Mode", "feature_description": "Add dark theme"})
    assert r.status_code == 200

    # 6. Добавляем пользователя (админская ручка)
    r = client.post("/add_user", params={"user_name": "testuser2"})
    assert r.status_code == 200

    # 7. Голосуем
    r = client.post("/add_vote", params={"feature_id": 1, "user_id": 1})
    assert r.status_code == 200

    # 8. Проверяем, что фича появилась
    r = client.get("/list_features")
    assert len(r.json()) == 1


def test_user_cannot_register_with_existing_name():
    """Проверяем, что нельзя зарегистрироваться с существующим именем"""
    client.post("/auth/register", data={"username": "uniqueuser", "password": "123456"})
    r = client.post("/auth/register", data={"username": "uniqueuser", "password": "123456"})
    assert r.status_code == 400


def test_login_with_wrong_password():
    """Проверяем, что вход с неправильным паролем не работает"""
    client.post("/auth/register", data={"username": "loginuser", "password": "correct"})
    r = client.post("/auth/login", data={"username": "loginuser", "password": "wrong"})
    assert r.status_code == 400
