from database.connection import db
from datetime import datetime
import uuid

loan_collection = db["loans"]

def create_loan(user_id, amount, interest_rate, term, status="pending"):
    loan = {
        "loan_id": str(uuid.uuid4()),
        "user_id": user_id,
        "amount": amount,
        "interest_rate": interest_rate,
        "term": term,
        "status": status,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    loan_collection.insert_one(loan)
    return loan

def get_loans_by_user(user_id):
    return list(loan_collection.find({"user_id": user_id}))

def get_loans_by_status(status):
    return list(loan_collection.find({"status": status}))

def update_loan_status(loan_id, status):
    loan_collection.update_one(
        {"loan_id": loan_id},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )