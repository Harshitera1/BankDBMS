import streamlit as st
from backend.controller.loan_controller import apply_for_loan
from backend.utils.auth import get_current_user

def loan_application_page():
    if "token" not in st.session_state:
        st.warning("Please login first.")
        return

    user_data = get_current_user(st.session_state.token)
    if not user_data:
        st.warning("Session expired. Please login again.")
        return

    st.title("💸 Apply for a Loan")

    amount = st.number_input("Loan Amount", min_value=1000.0, step=100.0)
    interest_rate = st.number_input("Interest Rate (%)", min_value=1.0, max_value=20.0, step=0.1)
    term = st.selectbox("Loan Term (months)", [12, 24, 36, 48, 60])

    if st.button("Apply for Loan"):
        success, message = apply_for_loan(user_data["user_id"], amount, interest_rate, term)
        if success:
            st.success(message)
        else:
            st.error(message)