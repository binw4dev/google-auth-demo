from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class GoogleLoginRequest(BaseModel):
    id_token: str

class UserSchema(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    name: str
    role: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TokenResponse(BaseModel):
    token: str
    user: UserSchema
