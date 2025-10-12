from pydantic import BaseModel, EmailStr

class GoogleLoginRequest(BaseModel):
    id_token: str

class UserResponse(BaseModel):
    email: EmailStr
    name: str
    role: str

class TokenResponse(BaseModel):
    token: str
    user: UserResponse