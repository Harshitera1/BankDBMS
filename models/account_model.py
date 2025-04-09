import random
from pymongo import MongoClient

class AccountModel:
    def __init__(self, db):
        self.collection = db['accounts']

    def generate_account_number(self):
        return str(random.randint(10**9, 10**10 - 1))  # 10-digit number

    def create_account(self, user_id, balance=0):
        account_number = self.generate_account_number()
        account = {
            "user_id": user_id,
            "account_number": account_number,
            "balance": balance
        }
        self.collection.insert_one(account)
        return account_number  # ✅ return it for reference

    def get_account_by_user_id(self, user_id):
        return self.collection.find_one({"user_id": user_id})

    def get_account_by_number(self, account_number):
        return self.collection.find_one({"account_number": account_number})

    def update_balance(self, account_number, new_balance):
        return self.collection.update_one(
            {"account_number": account_number},
            {"$set": {"balance": new_balance}}
        )

    def transfer_funds(self, from_acc_num, to_acc_num, amount):
        from_acc = self.get_account_by_number(from_acc_num)
        to_acc = self.get_account_by_number(to_acc_num)

        if from_acc and to_acc and from_acc["balance"] >= amount:
            self.update_balance(from_acc_num, from_acc["balance"] - amount)
            self.update_balance(to_acc_num, to_acc["balance"] + amount)
            return True
        return False
def get_account_by_number(self, account_number):
    return self.collection.find_one({"account_number": account_number})
