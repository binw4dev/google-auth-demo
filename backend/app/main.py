from fastapi import FastAPI, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import auth, dependencies
import os
import uvicorn
from app.main import app

fastapi_app = FastAPI()
fastapi_app.include_router(auth.router)

# 允许本地 React 前端访问
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@fastapi_app.get("/api/me")
def get_me(authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "")
    user = dependencies.get_current_user(token)
    return {"email": user.email, "name": user.name, "role": user.role}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)