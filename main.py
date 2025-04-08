import streamlit as st
from auth import signup_user, login_user
from transactions import get_user_balance, make_transaction, get_transactions

st.set_page_config(page_title="Bank Management System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

st.title("🏦 Bank Management System")

menu = ["Login", "Sign Up"] if not st.session_state.logged_in else ["Dashboard", "Logout"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Sign Up":
    st.subheader("Create a New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        success, msg = signup_user(username, password)
        st.success(msg) if success else st.error(msg)

elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        success, user = login_user(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

elif choice == "Dashboard":
    st.subheader(f"Welcome, {st.session_state.username}")
    balance = get_user_balance(st.session_state.username)
    st.info(f"Your current balance is: ₹{balance}")

    col1, col2 = st.columns(2)
    with col1:
        st.write("💰 Deposit")
        deposit_amount = st.number_input("Amount to Deposit", min_value=1)
        if st.button("Deposit"):
            success, msg = make_transaction(st.session_state.username, deposit_amount, "deposit")
            st.success(msg) if success else st.error(msg)

    with col2:
        st.write("💸 Withdraw")
        withdraw_amount = st.number_input("Amount to Withdraw", min_value=1)
        if st.button("Withdraw"):
            success, msg = make_transaction(st.session_state.username, withdraw_amount, "withdraw")
            st.success(msg) if success else st.error(msg)

    st.subheader("📋 Transaction History")
    transactions = get_transactions(st.session_state.username)
    for t in transactions:
        st.write(f"{t['date'].strftime('%Y-%m-%d %H:%M:%S')} - {t['type'].capitalize()} ₹{t['amount']}")

elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out.")
    st.rerun()
