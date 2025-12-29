from utils.file_handler import load_json, save_json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "..", "data", "users.json")


def get_all_users():
    return load_json(FILE)
def is_email_exists(email):
    users = get_all_users()
    return any(u["email"] == email for u in users)
def register_user(fullname, email, password):
    users = get_all_users()


    # Kiểm tra email trùng
    if is_email_exists(email):
        return False


    new_user = {
        "id": len(users) + 1,
        "name": fullname,
        "email": email,
        "password": password,
        "role": "student"
    }
    users.append(new_user)
    save_json(FILE, users)
    return True


def check_login(email, password):
    users = load_json(FILE)
    for user in users:
        if user['email'] == email and user['password'] == password:
            return user
    return None
