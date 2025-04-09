from backend.auth.jwt_handler import verify_token

def get_current_user(token):
    result = verify_token(token)
    if result["valid"]:
        return result["payload"]
    return None
