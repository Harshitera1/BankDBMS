import streamlit as st
from models.loan_model import get_loans_by_user
from backend.utils.auth import get_current_user

def my_loans_page():
    if "token" not in st.session_state:
        st.warning("Please login first.")
        return

    user_data = get_current_user(st.session_state.token)
    if not user_data:
        st.warning("Session expired. Please login again.")
        return

    st.title("📑 My Loans")

    loans = get_loans_by_user(user_data["user_id"])

    if not loans:
        st.info("You have no loans.")
    else:
        for loan in loans:
            st.subheader(f"Loan ID: {loan['loan_id']}")
            st.text(f"Amount: ₹{loan['amount']}")
            st.text(f"Interest Rate: {loan['interest_rate']}%")
            st.text(f"Term: {loan['term']} months")
            st.text(f"Status: {loan['status']}")
            st.text(f"Applied on: {loan['created_at'].strftime('%d %b %Y')}")