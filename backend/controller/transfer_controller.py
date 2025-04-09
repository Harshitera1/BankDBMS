from models.account_model import AccountModel
from models.transaction_model import record_transaction
from database.connection import db

account_model = AccountModel(db)

def transfer_funds(sender_id, receiver_id, amount, role):
    if role == "customer" and sender_id != receiver_id:
        return False, "Customers can only transfer from their own account."

    success = account_model.transfer_funds(sender_id, receiver_id, amount)
    if success:
        record_transaction(sender_id, receiver_id, amount)
        return True, "Transfer successful."
    return False, "Transfer failed due to insufficient balance or invalid accounts."
