from db import users_collection, transactions_collection
from datetime import datetime

def get_user_balance(username):
    user = users_collection.find_one({"username": username})
    return user.get("balance", 0)

def make_transaction(username, amount, type_):
    balance = get_user_balance(username)

    if type_ == "withdraw" and balance < amount:
        return False, "Insufficient balance"

    new_balance = balance + amount if type_ == "deposit" else balance - amount
    users_collection.update_one({"username": username}, {"$set": {"balance": new_balance}})
    
    transactions_collection.insert_one({
        "username": username,
        "type": type_,
        "amount": amount,
        "date": datetime.now()
    })
    
    return True, f"{type_.capitalize()} of {amount} successful."

def get_transactions(username):
    return list(transactions_collection.find({"username": username}))
