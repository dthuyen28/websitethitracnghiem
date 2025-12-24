from utils.file_handler import load_json, save_json

FILE = "data/users.json"

def register_user(name, email, password):
    users = load_json(FILE)

    # 1. kiểm tra email đã tồn tại chưa
    for user in users:
        if user['email'] == email:
            return False   # email đã tồn tại

    # 2. tạo user mới
    new_user = {
        "name": name,
        "email": email,
        "password": password
    }

    # 3. thêm vào danh sách
    users.append(new_user)

    # 4. lưu lại file json
    save_json(FILE, users)

    return True

def check_login(email, password):
    users = load_json(FILE)
    for user in users:
        if user['email'] == email and user['password'] == password:
            return user
    return None
