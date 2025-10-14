from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI, MONGO_DB

# create global async MongoDB client
client = AsyncIOMotorClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)

# database
db = client[MONGO_DB]

# collection for users
users_collection = db["users"]
