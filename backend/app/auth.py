from fastapi import APIRouter, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
from jose import jwt
from . import models, schemas, config
import logging

router = APIRouter(prefix="/api/auth", tags=["Auth"])
logger = logging.getLogger("app")  # 获取统一 logger

@router.post("/google", response_model=schemas.TokenResponse)
def google_login(payload: schemas.GoogleLoginRequest):
    logger.info(f"Received Google login request with id_token: {payload.id_token[:10]}...")  # Log part of the token for tracing
    id_token_str = payload.id_token
    try:
        idinfo = id_token.verify_oauth2_token(id_token_str, requests.Request(), config.GOOGLE_CLIENT_ID)
        google_sub = idinfo["sub"]
        email = idinfo.get("email")
        name = idinfo.get("name")

        # Search or create local user account
        if google_sub not in models.users_db:
            models.users_db[google_sub] = models.User(google_sub, email, name)
        user = models.users_db[google_sub]

        # Generate JWT
        token_data = {"sub": user.google_sub, "email": user.email, "role": user.role}
        token = jwt.encode(token_data, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

        logger.info(f"User {email} logged in successfully.")
        logger.debug(f"Generated JWT token: {token[:10]}...")  # Log part of the token for tracing

        return {"token": token, "user": user.__dict__}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google ID token")