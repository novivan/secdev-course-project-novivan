from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .model_dao_service import Model_dao_service

# preparing for app start
mds = Model_dao_service()

# start of the app
app = FastAPI(title="SecDev Course App", version="0.1.0")


class ApiError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        self.code = code
        self.message = message
        self.status = status


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Normalize FastAPI HTTPException into our error envelope
    detail = exc.detail if isinstance(exc.detail, str) else "http_error"
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": "http_error", "message": detail}},
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/add_user")
def add_user(user_name: str):
    mds.add_user(user_name)  # type: ignore


@app.post("/add_feature")
def add_feature(feature_title: str, feature_description: str):
    mds.add_feature(feature_title, feature_description)


@app.post("/add_vote")
def add_vote(feature_id: int, user_id: int):
    mds.add_vote(feature_id, user_id)


@app.get("/list_users")
def get_users():
    return mds.get_all_users()  # type: ignore


@app.get("/list_features")
def get_features():
    return mds.get_all_features()  # type: ignore


@app.get("/list_votes")
def get_votes():
    return mds.get_all_votes()  # type: ignore
