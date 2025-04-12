from database.connection import db
from datetime import datetime
import uuid

transaction_collection = db["transactions"]

def record_transaction(sender_id, receiver_id, amount):
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "amount": amount,
        "timestamp": datetime.utcnow()
    }
    transaction_collection.insert_one(transaction)

def get_transactions_by_user(user_id):
    return list(transaction_collection.find({
        "$or": [{"sender_id": user_id}, {"receiver_id": user_id}]
    }).sort("timestamp", -1))
def get_transactions_by_account(account_number):
    return list(transaction_collection.find({
        "$or": [{"sender_id": account_number}, {"receiver_id": account_number}]
    }).sort("timestamp", -1))

