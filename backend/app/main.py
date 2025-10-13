from fastapi import FastAPI, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import auth, dependencies
from app.core.logging_config import setup_logging

logger = setup_logging()

app = FastAPI()
app.include_router(auth.router)

# allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"https://google-auth-demo-frontend-dev.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/me")
def get_me(authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "")
    logger.debug(f"main get_me token: {token}")
    user = dependencies.get_current_user(token)
    logger.info(f"main get_me user: email{user.email}, name{user.name}, role{user.role}")
    return {"email": user.email, "name": user.name, "role": user.role}