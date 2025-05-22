print("🧪 Starting app...")

import streamlit as st

st.set_page_config(page_title="THE POT BANK", layout="wide")

# ✅ Add safe import handling with debug logs
try:
    print("🔄 Importing pages...")
    from frontend.pages.home import display_home
    from frontend.pages.login_popup import login_popup
    from frontend.pages.register import register_page
    from frontend.pages.dashboard import dashboard
    from frontend.pages.transfer import transfer_page
    from frontend.pages.view_users import view_users_page
    from frontend.pages.loan_application import loan_application_page
    from frontend.pages.my_loans import my_loans_page
    from frontend.pages.loan_management import loan_management_page
except Exception as e:
    st.error(f"🚨 Failed to import page modules: {e}")
    st.stop()

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

menu = ["🏠 Home", "🔐 Login", "📝 Register", "📊 Dashboard", "💸 Transfer", "👥 View Users", 
        "💸 Apply for Loan", "📑 My Loans", "🏦 Loan Management"]
default_index = menu.index(st.session_state.page)
choice = st.sidebar.selectbox("Navigate", menu, index=default_index)

# ✅ Logout button
if st.session_state.token:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.token = None
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.page = "🔐 Login"
        st.success("Logged out successfully.")
        st.stop()

# Page routing
if choice == "🏠 Home":
    st.session_state.page = "🏠 Home"
    display_home()
elif choice == "🔐 Login":
    st.session_state.page = "🔐 Login"
    login_popup()
elif choice == "📝 Register":
    st.session_state.page = "📝 Register"
    register_page()
elif choice == "📊 Dashboard":
    st.session_state.page = "📊 Dashboard"
    dashboard()
elif choice == "💸 Transfer":
    st.session_state.page = "💸 Transfer"
    transfer_page()
elif choice == "👥 View Users":
    st.session_state.page = "👥 View Users"
    view_users_page()
elif choice == "💸 Apply for Loan":
    st.session_state.page = "💸 Apply for Loan"
    loan_application_page()
elif choice == "📑 My Loans":
    st.session_state.page = "📑 My Loans"
    my_loans_page()
elif choice == "🏦 Loan Management":
    st.session_state.page = "🏦 Loan Management"
    loan_management_page()

print("🧪 App started successfully...")