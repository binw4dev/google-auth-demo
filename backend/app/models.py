from typing import Optional

class User:
    def __init__(self, google_sub: str, email: str, name: str, role: str = "user"):
        self.google_sub = google_sub
        self.email = email
        self.name = name
        self.role = role

users_db = {}  # memory DB: sub -> User