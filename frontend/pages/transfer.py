import streamlit as st
from backend.utils.auth import get_current_user
from backend.controller.transfer_controller import transfer_funds

def transfer_page():
    if "token" not in st.session_state:
        st.warning("Please login first.")
        return

    user_data = get_current_user(st.session_state.token)
    if not user_data:
        st.warning("Session expired. Please login again.")
        return

    st.title("💸 Transfer Funds")

    receiver_account_number = st.text_input("Receiver Account Number")
    amount = st.number_input("Amount to Transfer", min_value=1.0, step=1.0)

    if st.button("Transfer"):
        success, message = transfer_funds(
            sender_user_id=user_data["user_id"],
            receiver_account_number=receiver_account_number,
            amount=amount,
            role=user_data["role"]
        )
        if success:
            st.success(message)
        else:
            st.error(message)
