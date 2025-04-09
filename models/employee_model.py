from database.connection import db

employee_collection = db["employees"]  # ✅ Required

def create_employee(user_id, name, position, branch_id):
    employee_collection.insert_one({
        "user_id": user_id,
        "name": name,
        "position": position,
        "branch_id": branch_id
    })
