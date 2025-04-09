import uuid
from database.connection import db
from models.user_model import create_user
from models.account_model import AccountModel
from models.customer_model import create_customer
from models.employee_model import create_employee
from models.manager_model import create_manager

account_model = AccountModel(db)

def register_user(username, password, role, full_name, ifsc_code, email=None, position=None, account_number=None, initial_balance=0):
    try:
        user_id = str(uuid.uuid4())

        # Create user
        created = create_user(user_id, username, password, role)
        if not created:
            return False, "❌ Username already exists."

        if not account_number or len(account_number.strip()) < 6:
            return False, "❌ Please provide a valid account number (min 6 digits)."

        account_number = account_number.strip()

        existing = account_model.get_account_by_number(account_number)
        if existing:
            return False, f"❌ Account number `{account_number}` is already taken."

        # Create account
        account_model.collection.insert_one({
            "user_id": user_id,
            "account_number": account_number,
            "balance": initial_balance
        })

        # Role-specific profile creation
        if role == "customer":
            success, msg = create_customer(user_id, full_name, email, ifsc_code)
            return success, f"✅ Customer registered: {msg}\n🏦 Account Number: {account_number}\n💰 Initial Balance: ₹{initial_balance}"

        elif role == "employee":
            create_employee(user_id, full_name, position, ifsc_code)
            return True, f"✅ Employee registered.\n🏦 Account Number: {account_number}"

        elif role == "manager":
            create_manager(user_id, full_name, ifsc_code)
            return True, f"✅ Manager registered.\n🏦 Account Number: {account_number}"

        else:
            return False, "❌ Invalid role."

    except Exception as e:
        return False, f"❌ Error: {str(e)}"
