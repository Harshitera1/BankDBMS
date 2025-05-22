from models.loan_model import create_loan, update_loan_status
from models.user_model import find_user_by_id

def apply_for_loan(user_id, amount, interest_rate, term):
    user = find_user_by_id(user_id)
    if not user:
        return False, "User not found."
    loan = create_loan(user_id, amount, interest_rate, term)
    return True, "Loan application submitted."

def approve_loan(loan_id):
    update_loan_status(loan_id, "approved")
    return True, "Loan approved."

def reject_loan(loan_id):
    update_loan_status(loan_id, "rejected")
    return True, "Loan rejected."