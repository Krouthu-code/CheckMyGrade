"""
CheckMyGrade Application - Main Entry Point
Run this file to start the application.
"""

from login import LoginSystem
from menu import show_main_menu


def main():
    print("=" * 50)
    print("     Welcome to CheckMyGrade Application")
    print("=" * 50)

    login_system = LoginSystem()

    # Ask user to login or register
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            user = login_system.login()
            if user:
                show_main_menu(user)
        elif choice == "2":
            login_system.register()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
