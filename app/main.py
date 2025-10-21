from fastapi import Depends, FastAPI, HTTPException, Request

from . import auth
from .error_handler import problem
from .model import User
from .model_dao_service import mds

# start of the app
app = FastAPI(title="SecDev Course App", version="0.1.0")
app.include_router(auth.router)


class ApiError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        self.code = code
        self.message = message
        self.status = status


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return problem(status=exc.status, title=exc.code, detail=exc.message)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return problem(status=exc.status, title=exc.code, detail=exc.message)


@app.get("/health")
def health():
    return {"status": "ok"}


# === Защищенные ручки ===


@app.post("/add_user")
def add_user(user_name: str, current_user: User = Depends(auth.get_current_user)):
    mds.add_user(user_name)  # type: ignore


@app.post("/add_feature")
def add_feature(
    feature_title: str,
    feature_description: str,
    current_user: User = Depends(auth.get_current_user),
):
    mds.add_feature(feature_title, feature_description)


@app.post("/add_vote")
def add_vote(
    feature_id: int, user_id: int, current_user: User = Depends(auth.get_current_user)
):
    mds.add_vote(feature_id, user_id)


@app.post("/features/{feature_id}/vote")
def vote_for_feature(
    feature_id: int, current_user: User = Depends(auth.get_current_user)
):
    features = mds.get_all_features()
    if feature_id not in features:
        raise HTTPException(status_code=404, detail="Feature not found")

    user_id = current_user.get_id()
    # эта проверка должна срабатывать при любом запросе авторизованного пользователя
    # (просто на всякий пусть будет)
    users = mds.get_all_users()
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        mds.add_vote(feature_id, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"msg": "Vote recorded or updated"}


@app.get("/list_users")
def get_users(current_user: User = Depends(auth.get_current_user)):
    return mds.get_all_users()  # type: ignore


@app.get("/list_features")
def list_features(current_user: User = Depends(auth.get_current_user)):
    return mds.get_all_features()  # type: ignore


# комментарий для запуска CI
@app.get("/list_votes")
def get_votes(current_user: User = Depends(auth.get_current_user)):
    return mds.get_all_votes()  # type: ignore


# тут просто + форматирование и правильный путь к ручке (по тз)
@app.get("/features")
def get_features(current_user: User = Depends(auth.get_current_user)):
    features = mds.get_all_features()
    return [
        {"id": f.get_id(), "title": f.get_title(), "desc": f.get_description()}
        for f in features.values()
    ]
