import streamlit as st
from database.connection import db
import bcrypt
import os
from dotenv import load_dotenv
from backend.auth.jwt_handler import generate_token  # ✅ Reuse central function

load_dotenv()

def login_user(username, password):
    """Authenticate user with username and password"""
    user = db.users.find_one({"username": username})
    
    if not user:
        return {"status": False, "message": "Invalid credentials"}
    
    stored_password = user.get("password")
    if isinstance(stored_password, bytes) and bcrypt.checkpw(password.encode('utf-8'), stored_password):
        token = generate_token(user["user_id"], user["username"], user["role"])
        return {"status": True, "token": token, "role": user["role"]}
    elif user.get("password_raw") == password:
        token = generate_token(user["user_id"], user["username"], user["role"])
        return {"status": True, "token": token, "role": user["role"]}

    return {"status": False, "message": "Invalid credentials"}

def login_popup():
    """Display login form and handle authentication"""
    with st.expander("🔐 Login to THE POT BANK", expanded=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if not username or not password:
                st.error("Please enter both username and password")
                return
                
            result = login_user(username, password)
            if result["status"]:
                st.session_state.token = result["token"]
                st.session_state.role = result["role"]
                st.session_state.username = username
                st.success(f"Logged in as {result['role'].capitalize()}")
                st.session_state.page = "📊 Dashboard"
                st.stop()
            else:
                st.error(result["message"])
