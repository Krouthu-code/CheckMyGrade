"""
menu.py
Main menu and navigation logic for CheckMyGrade application.
Different menus are shown based on the user's role.
"""

from student import (
    add_new_student, delete_student, update_student_record,
    display_all_students, search_student, sort_students,
    check_my_grades, course_statistics
)
from course import add_new_course, delete_course, modify_course, display_all_courses
from professor import (
    add_new_professor, delete_professor, modify_professor,
    display_all_professors, show_course_details_by_professor
)
from grades import (
    display_grade_scale, report_by_course,
    report_by_student, report_by_professor
)


def show_main_menu(user):
    """Display the main menu based on the user's role."""
    while True:
        print(f"\n{'='*50}")
        print(f"  CheckMyGrade | Logged in as: {user.email} ({user.role})")
        print(f"{'='*50}")

        if user.role == "student":
            _student_menu(user)
        elif user.role == "professor":
            _professor_menu(user)
        elif user.role == "admin":
            _admin_menu(user)
        else:
            print("Unknown role. Logging out.")
            break


def _student_menu(user):
    """Menu for student users."""
    print("1. View my grades")
    print("2. Search a student record")
    print("3. View all courses")
    print("4. Change password")
    print("5. Logout")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        check_my_grades(user.email)
    elif choice == "2":
        search_student()
    elif choice == "3":
        display_all_courses()
    elif choice == "4":
        user.change_password()
    elif choice == "5":
        print("Logged out.")
        raise SystemExit


def _professor_menu(user):
    """Menu for professor users."""
    print("1. View all students")
    print("2. Add student")
    print("3. Delete student")
    print("4. Update student marks")
    print("5. Search student")
    print("6. Sort students")
    print("7. Course statistics")
    print("8. View my course students")
    print("9. Grade Reports")
    print("10. Change password")
    print("11. Logout")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        display_all_students()
    elif choice == "2":
        add_new_student()
    elif choice == "3":
        delete_student()
    elif choice == "4":
        update_student_record()
    elif choice == "5":
        search_student()
    elif choice == "6":
        sort_students()
    elif choice == "7":
        course_statistics()
    elif choice == "8":
        show_course_details_by_professor()
    elif choice == "9":
        _report_menu()
    elif choice == "10":
        user.change_password()
    elif choice == "11":
        print("Logged out.")
        raise SystemExit


def _admin_menu(user):
    """Menu for admin users - full access."""
    print("\n--- ADMIN MENU ---")
    print("1.  Student Management")
    print("2.  Course Management")
    print("3.  Professor Management")
    print("4.  Grade Reports")
    print("5.  Grade Scale")
    print("6.  Change password")
    print("7.  Logout")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        _student_management_menu()
    elif choice == "2":
        _course_management_menu()
    elif choice == "3":
        _professor_management_menu()
    elif choice == "4":
        _report_menu()
    elif choice == "5":
        display_grade_scale()
    elif choice == "6":
        user.change_password()
    elif choice == "7":
        print("Logged out.")
        raise SystemExit


def _student_management_menu():
    print("\n--- Student Management ---")
    print("1. View all students")
    print("2. Add student")
    print("3. Delete student")
    print("4. Update student marks")
    print("5. Search student")
    print("6. Sort students")
    print("7. Course statistics")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        display_all_students()
    elif choice == "2":
        add_new_student()
    elif choice == "3":
        delete_student()
    elif choice == "4":
        update_student_record()
    elif choice == "5":
        search_student()
    elif choice == "6":
        sort_students()
    elif choice == "7":
        course_statistics()


def _course_management_menu():
    print("\n--- Course Management ---")
    print("1. View all courses")
    print("2. Add course")
    print("3. Delete course")
    print("4. Modify course")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        display_all_courses()
    elif choice == "2":
        add_new_course()
    elif choice == "3":
        delete_course()
    elif choice == "4":
        modify_course()


def _professor_management_menu():
    print("\n--- Professor Management ---")
    print("1. View all professors")
    print("2. Add professor")
    print("3. Delete professor")
    print("4. Modify professor")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        display_all_professors()
    elif choice == "2":
        add_new_professor()
    elif choice == "3":
        delete_professor()
    elif choice == "4":
        modify_professor()


def _report_menu():
    print("\n--- Grade Reports ---")
    print("1. Report by course")
    print("2. Report by student")
    print("3. Report by professor")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        report_by_course()
    elif choice == "2":
        report_by_student()
    elif choice == "3":
        report_by_professor()
