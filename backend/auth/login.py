from models.user_model import find_user_by_username
from backend.auth.jwt_handler import generate_token
import bcrypt

def login_user(username, password):
    user = find_user_by_username(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        token = generate_token(user["user_id"], user["username"], user["role"])
        return {"status": True, "token": token, "role": user["role"]}
    return {"status": False, "message": "Invalid credentials"}
