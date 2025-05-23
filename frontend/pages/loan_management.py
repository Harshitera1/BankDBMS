import streamlit as st
from backend.controller.loan_controller import approve_loan, reject_loan
from models.loan_model import get_loans_by_status
from models.user_model import find_user_by_id, get_user_branch
from backend.utils.auth import get_current_user

def loan_management_page():
    if "token" not in st.session_state:
        st.warning("Please login first.")
        return

    user_data = get_current_user(st.session_state.token)
    if user_data["role"] not in ["manager", "employee"]:
        st.error("Unauthorized: Only managers and employees can manage loans.")
        return

    current_user_branch = get_user_branch(user_data["user_id"])
    if not current_user_branch:
        st.error("Could not determine your branch. Please contact support.")
        return

    st.title("🏦 Loan Management")

    # Get all pending loans
    pending_loans = get_loans_by_status("pending")
    
    # Filter loans to only include those from the same branch (for managers)
    filtered_loans = []
    for loan in pending_loans:
        loan_user_branch = get_user_branch(loan["user_id"])
        if loan_user_branch:
            # Managers can only manage loans from their own branch
            # Employees can manage all loans (no branch restriction)
            if user_data["role"] == "manager":
                if loan_user_branch == current_user_branch:
                    filtered_loans.append(loan)
            else:  # Employee role
                filtered_loans.append(loan)

    if not filtered_loans:
        st.info("No pending loans to manage from your branch.")
        return

    for loan in filtered_loans:
        user = find_user_by_id(loan["user_id"])
        username = user["username"] if user else "Unknown"
        st.subheader(f"Loan ID: {loan['loan_id']} - User: {username}")
        st.text(f"Amount: ₹{loan['amount']}")
        st.text(f"Interest Rate: {loan['interest_rate']}%")
        st.text(f"Term: {loan['term']} months")

        if st.button(f"Approve Loan {loan['loan_id']}"):
            # Double-check branch for managers before approving
            if user_data["role"] == "manager":
                loan_user_branch = get_user_branch(loan["user_id"])
                if loan_user_branch != current_user_branch:
                    st.error("You can only approve loans for users in your branch.")
                    continue

            success, message = approve_loan(loan['loan_id'])
            if success:
                st.success(message)
                st.experimental_rerun()  # Refresh the page to update the list
            else:
                st.error(message)

        if st.button(f"Reject Loan {loan['loan_id']}"):
            # Double-check branch for managers before rejecting
            if user_data["role"] == "manager":
                loan_user_branch = get_user_branch(loan["user_id"])
                if loan_user_branch != current_user_branch:
                    st.error("You can only reject loans for users in your branch.")
                    continue

            success, message = reject_loan(loan['loan_id'])
            if success:
                st.success(message)
                st.rerun()  # Refresh the page to update the list
            else:
                st.error(message)