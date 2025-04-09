from models.user_model import create_user
from models.account_model import AccountModel
from database.connection import db
import uuid

account_model = AccountModel(db)

def register_user(username, password, role):
    user_id = str(uuid.uuid4())
    created = create_user(user_id, username, password, role)
    if not created:
        return False, "Username already exists."

    # Create an account with default ₹0 balance
    account_model.create_account(user_id, 0)
    return True, "User and account created successfully."
