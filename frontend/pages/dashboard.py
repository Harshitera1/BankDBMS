import streamlit as st

def dashboard():
    st.title("📊 POT BANK Dashboard")

    if "token" not in st.session_state:
        st.warning("Please login first.")
        return

    st.success(f"Welcome to your dashboard, Role: {st.session_state.role}")
    if st.session_state.role == "manager":
        st.info("🔹 You have access to all accounts.")
    elif st.session_state.role == "employee":
        st.info("🔹 You can manage accounts and perform transfers.")
    elif st.session_state.role == "customer":
        st.info("🔹 You can only access your own account.")
