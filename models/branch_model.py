from db import db

branch_collection = db["branches"]

def create_branch(branch_name, location):
    if branch_collection.find_one({"branch_name": branch_name}):
        return False, "Branch already exists."
    branch_collection.insert_one({
        "branch_name": branch_name,
        "location": location
    })
    return True, "Branch created successfully."

def get_all_branches():
    return list(branch_collection.find())
