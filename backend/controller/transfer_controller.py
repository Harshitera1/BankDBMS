from models.account_model import AccountModel
from models.transaction_model import record_transaction
from database.connection import db

account_model = AccountModel(db)

def transfer_funds(sender_user_id, receiver_account_number, amount, role):
    sender_account = account_model.get_account_by_user_id(sender_user_id)

    # ✅ Safety check: ensure sender has a valid account with an account number
    if not sender_account or "account_number" not in sender_account:
        return False, "❌ Sender account is missing or invalid."

    sender_account_number = sender_account["account_number"]

    # ✅ Prevent self-transfer for customers
    if role == "customer" and sender_account_number == receiver_account_number:
        return False, "❌ Customers cannot transfer to their own account."

    # ✅ Proceed with transfer
    success = account_model.transfer_funds(sender_account_number, receiver_account_number, amount)
    if success:
        record_transaction(sender_account_number, receiver_account_number, amount)
        return True, "✅ Transfer successful."
    else:
        return False, "❌ Transfer failed due to insufficient balance or invalid accounts."
