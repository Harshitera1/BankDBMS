from database.connection import db

branch_collection = db["branches"]

def create_branch(branch_name, location):
    existing = branch_collection.find_one({"branch_name": branch_name})
    if existing:
        return False, "Branch already exists."
    branch_collection.insert_one({"branch_name": branch_name, "location": location})
    return True, "Branch created."
