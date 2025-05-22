from database.connection import db
import bcrypt

user_collection = db["users"]
manager_collection = db["managers"]
employee_collection = db["employees"]
customer_collection = db["customers"]

def create_user(user_id, username, password, role):
    if len(password) < 6:
        return False  # ✅ Reject short passwords

    existing = user_collection.find_one({"username": username})
    if existing:
        return False

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_collection.insert_one({
        "user_id": user_id,
        "username": username,
        "password": hashed,        # ✅ Hashed password for login
        "password_raw": password,  # ✅ Visible in DB for admin/testing only
        "role": role
    })
    return True

def find_user_by_username(username):
    return user_collection.find_one({"username": username})

def find_user_by_id(user_id):
    return user_collection.find_one({"user_id": user_id})

def get_user_branch(user_id):
    # Find the user in the users collection to get their role
    user = find_user_by_id(user_id)
    if not user:
        return None

    role = user["role"]
    branch_id = None

    # Fetch branch_id based on the user's role
    if role == "manager":
        manager = manager_collection.find_one({"user_id": user_id})
        branch_id = manager["branch_id"] if manager else None
    elif role == "employee":
        employee = employee_collection.find_one({"user_id": user_id})
        branch_id = employee["branch_id"] if employee else None
    elif role == "customer":
        customer = customer_collection.find_one({"user_id": user_id})
        branch_id = customer["branch_id"] if customer else None

    return branch_id