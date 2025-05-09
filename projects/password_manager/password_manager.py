import os
import json
import getpass
import base64
from cryptography.fernet import Fernet, InvalidToken
import hashlib
import re

DATA_FILE = 'vault.dat'
SALT_FILE = 'salt.bin'

# Password strength checker
def check_strength(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain a digit."
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\",.<>/?]", password):
        return False, "Password must contain a special character."
    return True, "Strong password."

def derive_key(master_password, salt):
    # Derive a key from the master password and salt
    kdf = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100_000)
    return base64.urlsafe_b64encode(kdf)

def load_salt():
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, 'wb') as f:
            f.write(salt)
    else:
        with open(SALT_FILE, 'rb') as f:
            salt = f.read()
    return salt

def load_vault(fernet):
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'rb') as f:
        encrypted = f.read()
    try:
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except (InvalidToken, json.JSONDecodeError):
        print("[!] Failed to decrypt vault. Wrong master password?")
        return None

def save_vault(vault, fernet):
    data = json.dumps(vault).encode()
    encrypted = fernet.encrypt(data)
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypted)

def add_password(vault):
    site = input("Site: ").strip()
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    ok, msg = check_strength(password)
    if not ok:
        print(f"[!] {msg}")
        return
    vault[site] = {'username': username, 'password': password}
    print(f"[+] Added credentials for {site}.")

def retrieve_password(vault):
    site = input("Site: ").strip()
    if site in vault:
        print(f"Username: {vault[site]['username']}")
        print(f"Password: {vault[site]['password']}")
    else:
        print("[!] No credentials found for that site.")

def delete_password(vault):
    site = input("Site: ").strip()
    if site in vault:
        del vault[site]
        print(f"[+] Deleted credentials for {site}.")
    else:
        print("[!] No credentials found for that site.")

def main():
    print("=== Quiara's Password Manager ===")
    salt = load_salt()
    master_password = getpass.getpass("Enter master password: ")
    key = derive_key(master_password, salt)
    fernet = Fernet(key)
    vault = load_vault(fernet)
    if vault is None:
        return
    while True:
        print("\nOptions: [A]dd, [R]etrieve, [D]elete, [L]ist, [Q]uit")
        choice = input(">> ").strip().lower()
        if choice == 'a':
            add_password(vault)
            save_vault(vault, fernet)
        elif choice == 'r':
            retrieve_password(vault)
        elif choice == 'd':
            delete_password(vault)
            save_vault(vault, fernet)
        elif choice == 'l':
            print("Sites:", ', '.join(vault.keys()) if vault else "No entries.")
        elif choice == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main() 