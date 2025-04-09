from pymongo import MongoClient
from bson import ObjectId

class AccountModel:
    def __init__(self, db):
        self.collection = db['accounts']

    def create_account(self, user_id, balance=0):
        account = {
            "user_id": user_id,
            "balance": balance
        }
        return self.collection.insert_one(account).inserted_id

    def get_account_by_user_id(self, user_id):
        return self.collection.find_one({"user_id": user_id})

    def update_balance(self, user_id, new_balance):
        return self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"balance": new_balance}}
        )

    def transfer_funds(self, from_user_id, to_user_id, amount):
        from_acc = self.get_account_by_user_id(from_user_id)
        to_acc = self.get_account_by_user_id(to_user_id)

        if from_acc and to_acc and from_acc["balance"] >= amount:
            self.update_balance(from_user_id, from_acc["balance"] - amount)
            self.update_balance(to_user_id, to_acc["balance"] + amount)
            return True
        return False
