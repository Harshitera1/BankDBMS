from database.connection import db

branch_collection = db["branches"]

def create_branch(branch_name, ifsc_code, location):
    existing = branch_collection.find_one({"ifsc_code": ifsc_code})
    if existing:
        return False, "Branch already exists."
    branch_collection.insert_one({
        "branch_name": branch_name,
        "ifsc_code": ifsc_code,
        "location": location
    })
    return True, "Branch created."

def get_all_branches():
    return list(branch_collection.find({}))
