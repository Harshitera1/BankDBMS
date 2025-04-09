import streamlit as st
from backend.utils.auth import get_current_user
from database.connection import db

def dashboard():
    st.title("📊 POT BANK Dashboard")

    if "token" not in st.session_state:
        st.warning("Please login first.")
        return

    user_data = get_current_user(st.session_state.token)
    if not user_data:
        st.warning("Session expired. Please login again.")
        return

    st.success(f"Welcome, {user_data['username']} ({user_data['role']})")

    # 🏦 Load account details
    account = db.accounts.find_one({"user_id": user_data["user_id"]})
    if account:
        st.subheader("💳 Account Info")
        st.text(f"Account Number: {account.get('account_number')}")
        st.text(f"Balance: ₹{account.get('balance', 0)}")
    else:
        st.warning("No account found.")

    # 🏢 Branch Info
    branch = db.branches.find_one({"ifsc_code": user_data.get("branch_id")})
    if branch:
        st.subheader("🏢 Branch Info")
        st.text(f"Branch Name: {branch.get('branch_name')}")
        st.text(f"IFSC Code: {branch.get('ifsc_code')}")

    # 📋 Schemes and Benefits
    schemes = db.get_collection("schemes").find()
    st.subheader("📄 Bank Schemes & Benefits")

    for scheme in schemes:
        st.markdown(f"**📝 {scheme['name']}** — {scheme['description']}")

    # ✏️ Manager access
    if user_data["role"] == "manager":
        st.markdown("---")
        st.subheader("🔧 Manage Schemes")

        name = st.text_input("Scheme Name")
        description = st.text_area("Description")

        if st.button("Add Scheme"):
            db.get_collection("schemes").insert_one({"name": name, "description": description})
            st.success("✅ Scheme added.")
