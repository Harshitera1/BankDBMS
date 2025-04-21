import streamlit as st
from backend.utils.auth import get_current_user
from backend.controller.transfer_controller import transfer_funds
from models.transaction_model import get_transactions_by_account
from models.account_model import AccountModel
from database.connection import db

account_model = AccountModel(db)

def transfer_page():
    if "token" not in st.session_state:
        st.warning("Please login first.")
        return

    user_data = get_current_user(st.session_state.token)
    if not user_data:
        st.warning("Session expired. Please login again.")
        return

    st.title("💸 Transfer Funds")

    sender_account = account_model.get_account_by_user_id(user_data["user_id"])
    if not sender_account:
        st.error("❌ Your account was not found.")
        return

    sender_account_number = sender_account.get("account_number")
    if not sender_account_number:
        st.error("❌ Your account is missing an account number.")
        return

    st.markdown("### 🧾 Send Money")
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

    # 🔍 Transaction History
    st.markdown("---")
    st.subheader("📄 Transaction History")
    transactions = get_transactions_by_account(sender_account_number)

    if not transactions:
        st.info("No transactions to show.")
    else:
        for tx in transactions[:10]:
            direction = "🔺 Sent" if tx["sender_id"] == sender_account_number else "🔻 Received"
            other_party = tx["receiver_id"] if direction == "🔺 Sent" else tx["sender_id"]
            st.markdown(f"""
                **{direction} ₹{tx['amount']}**  
                ↔️ With: `{other_party}`  
                🕒 {tx['timestamp'].strftime("%d %b %Y, %I:%M %p")}
                ---
            """)
