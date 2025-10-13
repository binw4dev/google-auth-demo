import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
JWT_SECRET = os.getenv("JWT_SECRET", "secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://binw4dev_db_user:Wcwe1IgdkVh5CsHr@bavilion-cluster-dev.cuylfau.mongodb.net/?retryWrites=true&w=majority&appName=bavilion-cluster-dev")
MONGO_DB = os.getenv("MONGO_DB", "google-auth-demo")