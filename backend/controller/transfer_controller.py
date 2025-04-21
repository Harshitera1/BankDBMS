from models.account_model import AccountModel
from models.transaction_model import record_transaction
from database.connection import db

account_model = AccountModel(db)

def transfer_funds(sender_user_id, receiver_account_number, amount, role):
    sender_account = account_model.get_account_by_user_id(sender_user_id)

    if not sender_account or "account_number" not in sender_account:
        return False, "❌ Sender account is missing or invalid."

    sender_account_number = sender_account["account_number"]

    # ✅ Allow self-transfer but treat it as internal transaction
    if sender_account_number == receiver_account_number:
        record_transaction(sender_account_number, receiver_account_number, amount)
        return True, "🔁 Funds transferred to your own account."

    success = account_model.transfer_funds(sender_account_number, receiver_account_number, amount)
    if success:
        record_transaction(sender_account_number, receiver_account_number, amount)
        return True, "✅ Transfer successful."
    else:
        return False, "❌ Transfer failed due to insufficient balance or invalid accounts."
