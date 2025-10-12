from fastapi import FastAPI, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import auth, dependencies

app = FastAPI()
app.include_router(auth.router)

# 允许本地 React 前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/me")
def get_me(authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "")
    user = dependencies.get_current_user(token)
    return {"email": user.email, "name": user.name, "role": user.role}