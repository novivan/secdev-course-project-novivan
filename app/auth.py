from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .model import User, pwd_context
from .model_dao_service import mds

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "your-super-secret-key-change-in-production"
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
    if len(password) > 72:
        raise HTTPException(
            status_code=400, detail="Password too long (max 72 characters)"
        )
    if len(password) < 4:
        raise HTTPException(status_code=400, detail="Password is too short")

    try:
        mds.add_user(username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    users = mds.get_all_users()
    user = next((u for u in users.values() if u.get_name() == username), None)
    if user is None:
        raise HTTPException(status_code=500, detail="User created but not found")

    user._hashed_password = pwd_context.hash(password)
    return {"msg": "User created. Now you can <a href='/auth/login'>log in</a>."}


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
