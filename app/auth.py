from datetime import datetime, timedelta
from os import getenv

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from .model import User
from .model_dao_service import mds

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = getenv("JWT_SECRET", "fallback_dev_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    users = mds.get_all_users()
    user = next((u for u in users.values() if u.get_name() == username), None)
    if user is None:
        raise credentials_exception
    return user


@router.get("/login")
def get_login_page():
    return HTMLResponse(content=HTML_LOGIN_FORM)


@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    users = mds.get_all_users()
    user = next((u for u in users.values() if u.get_name() == username), None)
    if not user or not user.verify_password(password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_access_token(data={"sub": user.get_name()})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/register")
def get_register_page():
    return HTMLResponse(content=HTML_REGISTER_FORM)


@router.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    print(
        f"Registering user: {username}, password length: {len(password)}"
    )  # Debug output
    if len(username) < 4:
        raise HTTPException(
            status_code=400, detail="Username is too short (minimum 4 characters)"
        )
    if len(username) > 20:
        raise HTTPException(
            status_code=400, detail="Username is too long (maximum 20 characters)"
        )
    if len(password) > 72:
        raise HTTPException(
            status_code=400, detail="Password too long (max 72 characters)"
        )
    if len(password) < 4:
        raise HTTPException(status_code=400, detail="Password is too short")

    try:
        print(f"Registering user: {username}, password length: {len(password)}")

        if mds.get_user_by_username(username):
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = pwd_context.hash(password)

        # Use instance method
        mds.add_user(username=username, user_hashsed_password=hashed_password)

        return {"msg": "User created successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# HTML-формы
HTML_LOGIN_FORM = """
<!DOCTYPE html>
<html>
<head><title>Вход</title></head>
<body>
<h2>Войти</h2>
<form method="post" action="/auth/login">
    <label>Логин: <input type="text" name="username" required></label><br><br>
    <label>Пароль: <input type="password" name="password" required></label><br><br>
    <button type="submit">Войти</button>
</form>
<p><a href="/auth/register">Зарегистрироваться</a></p>
</body>
</html>
"""

HTML_REGISTER_FORM = """
<!DOCTYPE html>
<html>
<head><title>Регистрация</title></head>
<body>
<h2>Регистрация</h2>
<form method="post" action="/auth/register">
    <label>Логин: <input type="text" name="username" required></label><br><br>
    <label>Пароль: <input type="password" name="password" required></label><br><br>
    <button type="submit">Зарегистрироваться</button>
</form>
<p><a href="/auth/login">Войти</a></p>
</body>
</html>
"""
