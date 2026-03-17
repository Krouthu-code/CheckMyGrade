"""
login.py
Handles user login, logout, and registration.
Uses login.csv to store user credentials.
"""

from csv_helper import read_csv, write_csv, append_csv
from encryption import encrypt_password, decrypt_password

LOGIN_FILE = "login.csv"
LOGIN_FIELDS = ["email", "password", "role"]


class LoginUser:
    def __init__(self, email, password, role):
        self.email = email
        self.password = password  # This is the plain-text password in memory
        self.role = role

    def change_password(self):
        """Allow the logged-in user to change their password."""
        old_pass = input("Enter current password: ").strip()
        if old_pass != self.password:
            print("Incorrect current password.")
            return

        new_pass = input("Enter new password: ").strip()
        if not new_pass:
            print("Password cannot be empty.")
            return

        # Update in file
        rows = read_csv(LOGIN_FILE)
        for row in rows:
            if row["email"] == self.email:
                row["password"] = encrypt_password(new_pass)
        write_csv(LOGIN_FILE, rows, LOGIN_FIELDS)
        self.password = new_pass
        print("Password changed successfully!")


class LoginSystem:
    def login(self):
        """Log in a user. Returns a LoginUser object if successful."""
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()

        rows = read_csv(LOGIN_FILE)
        for row in rows:
            decrypted = decrypt_password(row["password"])
            if row["email"] == email and decrypted == password:
                print(f"\nLogin successful! Welcome, {email} ({row['role']})")
                return LoginUser(email, password, row["role"])

        print("Invalid email or password.")
        return None

    def register(self):
        """Register a new user."""
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()
        role = input("Enter role (student/professor/admin): ").strip().lower()

        if not email or not password or role not in ["student", "professor", "admin"]:
            print("Invalid input. Registration failed.")
            return

        # Check if email already exists
        rows = read_csv(LOGIN_FILE)
        for row in rows:
            if row["email"] == email:
                print("Email already registered.")
                return

        encrypted = encrypt_password(password)
        append_csv(LOGIN_FILE, {"email": email, "password": encrypted, "role": role}, LOGIN_FIELDS)
        print(f"Registered successfully as {role}!")

    def logout(self, user):
        """Log out the user."""
        print(f"Goodbye, {user.email}!")
        return None
