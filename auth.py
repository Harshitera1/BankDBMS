import bcrypt
from db import users_collection

def signup_user(username, password):
    if users_collection.find_one({"username": username}):
        return False, "Username already exists."
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({"username": username, "password": hashed, "balance": 0})
    return True, "User created successfully."

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return True, user
    return False, None
