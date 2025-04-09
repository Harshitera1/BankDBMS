from database.connection import db

customer_collection = db["customers"]

def create_customer(user_id, full_name, email, branch_id):
    existing = customer_collection.find_one({"user_id": user_id})
    if existing:
        return False, "Customer already exists."
    customer_collection.insert_one({
        "user_id": user_id,
        "full_name": full_name,
        "email": email,
        "branch_id": branch_id
    })
    return True, "Customer profile created."
