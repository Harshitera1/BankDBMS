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
        st.subheader(f"👤 {user['username']} ({user['role']})")
        st.text(f"User ID: {user['user_id']}")
        if user['user_id'] in accounts:
            acc = accounts[user['user_id']]
            st.text(f"💰 Account Balance: ₹{acc['balance']}")
        else:
            st.warning("❗ No account linked.")
