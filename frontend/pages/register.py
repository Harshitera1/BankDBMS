import streamlit as st
from backend.controller.user_controller import register_user
from models.branch_model import get_all_branches

def register_page():
    st.title("📝 Register New User")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email (Customer Only)")

    branches = get_all_branches()
    ifsc_codes = [branch["ifsc"] for branch in branches]
    ifsc_code = st.selectbox("Select Bank IFSC Code", ifsc_codes)

    role = st.selectbox("Select Role", ["customer", "employee", "manager"])
    position = st.text_input("Position (Employee Only)") if role == "employee" else None
    account_number = st.text_input("Account Number")
    initial_balance = st.number_input("Initial Account Balance", min_value=0.0)

    if st.button("Register"):
        success, message = register_user(
            username=username,
            password=password,
            role=role,
            full_name=full_name,
            email=email,
            ifsc_code=ifsc_code,
            position=position,
            account_number=account_number,
            initial_balance=initial_balance
        )

        if success:
            st.success(message)
            st.session_state.page = "🔐 Login"  # Redirect to login
            st.stop()  # Safe fallback instead of experimental_rerun
        else:
            st.error(message)
