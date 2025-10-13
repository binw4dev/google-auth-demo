from fastapi import APIRouter, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
from jose import jwt
from datetime import datetime
from . import config, database, schemas, models
import logging

logger = logging.getLogger("app")  # get logger
router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/google", response_model=schemas.TokenResponse)
async def google_login(payload: schemas.GoogleLoginRequest):
    logger.info(f"Received Google login request with id_token: {payload.id_token[:10]}...")  # Log part of the token for tracing
    try:
        # 验证Google ID Token
        idinfo = id_token.verify_oauth2_token(
            payload.id_token,
            requests.Request(),
            config.GOOGLE_CLIENT_ID
        )

        google_sub = idinfo["sub"]
        email = idinfo.get("email")
        name = idinfo.get("name")

        # 查询是否已存在用户
        existing_user = await database.users_collection.find_one({"sub": google_sub})

        if existing_user:
            # 更新用户信息
            await database.users_collection.update_one(
                {"sub": google_sub},
                {"$set": {"name": name, "email": email, "updated_at": datetime.utcnow()}}
            )
            user = await database.users_collection.find_one({"sub": google_sub})
        else:
            # 创建新用户
            new_user = {
                "sub": google_sub,
                "email": email,
                "name": name,
                "role": "user",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            result = await database.users_collection.insert_one(new_user)
            user = await database.users_collection.find_one({"_id": result.inserted_id})

        # 生成JWT
        token_data = {"sub": user["sub"], "email": user["email"], "role": user["role"]}
        token = jwt.encode(token_data, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

        logger.info(f"User {email} logged in successfully.")
        logger.debug(f"Generated JWT token: {token[:10]}...")  # Log part of the token for tracing

        return {"token": token, "user": models.user_dict(user)}

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google ID token")