import json
import os
from cryptography.fernet import Fernet

KEY_FILE = "key.key"
DATA_FILE = "passwords.json"

WEBSITE = "gmail.com"
USERNAME = "intern_user@gmail.com"
PASSWORD = "Secure@123"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

key = load_key()
fernet = Fernet(key)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "rb") as file:
        encrypted_data = file.read()
        if not encrypted_data:
            return {}
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data)

def save_data(data):
    encrypted_data = fernet.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, "wb") as file:
        file.write(encrypted_data)

def add_password():
    data = load_data()
    data[WEBSITE] = {
        "username": USERNAME,
        "password": PASSWORD
    }
    save_data(data)
    print("[✔] Password saved successfully")

def get_password():
    data = load_data()
    print("[✔] Website :", WEBSITE)
    print("[✔] Username:", data[WEBSITE]["username"])
    print("[✔] Password:", data[WEBSITE]["password"])

def delete_password():
    data = load_data()
    del data[WEBSITE]
    save_data(data)
    print("[✔] Password deleted successfully")

print("\n--- PASSWORD MANAGER DEMO ---\n")
add_password()
get_password()
delete_password()
print("\n--- TASK COMPLETED ---")