from database.connection import db

manager_collection = db["managers"]

def create_manager(user_id, name, branch_id):
    manager_collection.insert_one({
        "user_id": user_id,
        "name": name,
        "branch_id": branch_id
    })
