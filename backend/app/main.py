from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import auth, dependencies
from app.core.logging_config import setup_logging
from .config import ALLOW_CORS

logger = setup_logging()

app = FastAPI()
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOW_CORS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/me")
async def get_me(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    token = authorization.replace("Bearer ", "")
    logger.debug(f"main get_me token: {token}")
    user = await dependencies.get_current_user(token)
    logger.info(f"main get_me user: email: {user['email']}, name: {user['name']}, role: {user['role']}")
    return user
