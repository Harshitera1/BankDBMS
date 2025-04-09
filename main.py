import streamlit as st

# ✅ THIS MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="THE POT BANK", layout="wide")

# ✅ NOW YOU CAN IMPORT YOUR FRONTEND MODULES
from frontend.pages.home import display_home
from frontend.pages.login_popup import login_popup
from frontend.pages.dashboard import dashboard
from frontend.pages.transfer import transfer_page

# Setup session state
if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.username = None

menu = ["🏠 Home", "🔐 Login", "📊 Dashboard", "💸 Transfer"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "🏠 Home":
    display_home()
elif choice == "🔐 Login":
    login_popup()
elif choice == "📊 Dashboard":
    dashboard()
elif choice == "💸 Transfer":
    transfer_page()
