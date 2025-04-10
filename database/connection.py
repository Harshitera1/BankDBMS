from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["bankDB"]

try:
    print("🔌 Mongo connected to:", db.list_collection_names())
except Exception as e:
    print("❌ MongoDB connection failed:", e)
