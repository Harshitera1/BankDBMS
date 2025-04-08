from db import db

manager_collection = db["managers"]

def create_manager(manager_name, branch_id):
    if manager_collection.find_one({"branch_id": branch_id}):
        return False, "This branch already has a manager."

    manager_collection.insert_one({
        "manager_name": manager_name,
        "branch_id": branch_id
    })
    return True, "Manager assigned to branch successfully."

def get_manager_by_branch(branch_id):
    return manager_collection.find_one({"branch_id": branch_id})
