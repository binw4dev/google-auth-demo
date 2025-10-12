from fastapi import FastAPI, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import auth, dependencies
import uvicorn
import os

app = FastAPI()
app.include_router(auth.router)

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)