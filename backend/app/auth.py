from fastapi import APIRouter, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
from jose import jwt
from . import models, schemas, config

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/google", response_model=schemas.TokenResponse)
def google_login(payload: schemas.GoogleLoginRequest):
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

        return {"token": token, "user": user.__dict__}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google ID token")