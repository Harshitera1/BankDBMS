from database.connection import db
import bcrypt

user_collection = db["users"]

def create_user(user_id, username, password, role):
    existing = user_collection.find_one({"username": username})
    if existing:
        return False
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_collection.insert_one({
        "user_id": user_id,
        "username": username,
        "password": hashed,
        "role": role
    })
    return True

def find_user_by_username(username):
    return user_collection.find_one({"username": username})
