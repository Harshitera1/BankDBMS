import streamlit as st
from database.connection import db

def view_users_page():
    if st.session_state.get("role") != "manager":
        st.error("Unauthorized: Only managers can view users.")
        return

    st.title("👥 All Users and Accounts")

    users = list(db["users"].find())
    accounts = {acc["user_id"]: acc for acc in db["accounts"].find()}

    for user in users:
        st.markdown("---")

        # ✅ Safely handle missing fields
        username = user.get("username", "Unknown")
        role = user.get("role", "unknown")
        user_id = user.get("user_id", "N/A")

        st.subheader(f"👤 {username} ({role})")
        st.text(f"User ID: {user_id}")

        if user_id in accounts:
            acc = accounts[user_id]
            st.text(f"🏦 Account Number: {acc.get('account_number', 'N/A')}")
            st.text(f"💰 Balance: ₹{acc.get('balance', 0)}")
        else:
            st.warning("❗ No account linked.")
