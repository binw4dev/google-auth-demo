from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from . import config, models

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        sub = payload.get("sub")
        if sub not in models.users_db:
            raise HTTPException(status_code=401, detail="User not found")
        return models.users_db[sub]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")