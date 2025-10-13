from fastapi import HTTPException
from jose import jwt, JWTError
from . import config, database, models

import logging

logger = logging.getLogger("app")

async def get_current_user(token: str):
    logger.debug(f"get_current_user token: {token}")
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        sub = payload.get("sub")
        user = await database.users_collection.find_one({"sub": sub})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        logger.debug(f"get_current_user payload: {payload}")
        return models.user_dict(user)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
