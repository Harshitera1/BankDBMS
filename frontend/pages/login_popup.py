import streamlit as st
from backend.auth.login import login_user

def login_popup():
    with st.expander("🔐 Login to THE POT BANK", expanded=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login_user(username, password)
            if result["status"]:
                st.session_state.token = result["token"]
                st.session_state.role = result["role"]
                st.session_state.username = username
                st.success(f"Logged in as {result['role'].capitalize()}")

                # ✅ Redirect safely to Dashboard
                st.session_state.page = "📊 Dashboard"
                st.stop()  # Safe fallback (halts and refreshes)
            else:
                st.error(result["message"])
