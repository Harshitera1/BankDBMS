import streamlit as st

st.set_page_config(page_title="THE POT BANK", layout="wide")

# Page imports
from frontend.pages.home import display_home
from frontend.pages.login_popup import login_popup
from frontend.pages.register import register_page
from frontend.pages.dashboard import dashboard
from frontend.pages.transfer import transfer_page
from frontend.pages.view_users import view_users_page

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

menu = ["🏠 Home", "🔐 Login", "📝 Register", "📊 Dashboard", "💸 Transfer", "👥 View Users"]
default_index = menu.index(st.session_state.page)
choice = st.sidebar.selectbox("Navigate", menu, index=default_index)
# ✅ Optional logout button
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
