from datetime import datetime
from typing import Optional
from bson import ObjectId

def user_dict(user) -> dict:
    """Convert MongoDB document to JSON-safe dict"""
    if not user:
        return None
    user["_id"] = str(user["_id"])
    return user

class UserModel:
    def __init__(self, sub: str, email: str, name: str, role: str = "user"):
        self.sub = sub
        self.email = email
        self.name = name
        self.role = role
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
