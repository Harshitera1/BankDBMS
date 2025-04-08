from db import db

customer_collection = db["customers"]

def create_customer(username, full_name, email, branch_id):
    if customer_collection.find_one({"username": username}):
        return False, "Customer already exists."

    customer_collection.insert_one({
        "username": username,
        "full_name": full_name,
        "email": email,
        "branch_id": branch_id,
    })
    return True, "Customer created successfully."

def get_customer(username):
    return customer_collection.find_one({"username": username})
