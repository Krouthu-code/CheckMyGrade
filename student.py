"""
student.py
Student class with all student-related operations.
Students are stored in students.csv
"""

from csv_helper import read_csv, write_csv, append_csv

STUDENT_FILE = "students.csv"
STUDENT_FIELDS = ["email", "first_name", "last_name", "course_id", "grade", "marks"]


def get_letter_grade(marks):
    """Return letter grade based on marks."""
    marks = float(marks)
    if marks >= 90:
        return "A"
    elif marks >= 80:
        return "B"
    elif marks >= 70:
        return "C"
    elif marks >= 60:
        return "D"
    else:
        return "F"


class Student:
    def __init__(self, email, first_name, last_name, course_id, grade, marks):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.course_id = course_id
        self.grade = grade
        self.marks = marks

    def display_records(self):
        """Print this student's record."""
        print(f"  Email     : {self.email}")
        print(f"  Name      : {self.first_name} {self.last_name}")
        print(f"  Course    : {self.course_id}")
        print(f"  Grade     : {self.grade}")
        print(f"  Marks     : {self.marks}")

    def to_dict(self):
        """Convert student to dictionary for CSV writing."""
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "course_id": self.course_id,
            "grade": self.grade,
            "marks": self.marks,
        }


# ─── CRUD Operations ─────────────────────────────────────────────────────────

def add_new_student():
    """Add a new student record."""
    email = input("Student email: ").strip()
    if not email:
        print("Email cannot be empty.")
        return

    # Check for duplicate email
    rows = read_csv(STUDENT_FILE)
    for row in rows:
        if row["email"] == email:
            print("A student with this email already exists.")
            return

    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    course_id = input("Course ID: ").strip()
    marks = input("Marks (0-100): ").strip()

    try:
        marks_float = float(marks)
    except ValueError:
        print("Invalid marks. Must be a number.")
        return

    grade = get_letter_grade(marks_float)
    student = Student(email, first_name, last_name, course_id, grade, marks)
    append_csv(STUDENT_FILE, student.to_dict(), STUDENT_FIELDS)
    print(f"Student {first_name} {last_name} added successfully!")


def delete_student():
    """Delete a student by email."""
    email = input("Enter student email to delete: ").strip()
    rows = read_csv(STUDENT_FILE)
    new_rows = [row for row in rows if row["email"] != email]

    if len(new_rows) == len(rows):
        print("Student not found.")
    else:
        write_csv(STUDENT_FILE, new_rows, STUDENT_FIELDS)
        print("Student deleted successfully.")


def update_student_record():
    """Update a student's marks and grade."""
    email = input("Enter student email to update: ").strip()
    rows = read_csv(STUDENT_FILE)
    found = False

    for row in rows:
        if row["email"] == email:
            found = True
            print(f"Current marks: {row['marks']}")
            new_marks = input("Enter new marks (0-100): ").strip()
            try:
                marks_float = float(new_marks)
            except ValueError:
                print("Invalid marks.")
                return
            row["marks"] = new_marks
            row["grade"] = get_letter_grade(marks_float)
            break

    if not found:
        print("Student not found.")
    else:
        write_csv(STUDENT_FILE, rows, STUDENT_FIELDS)
        print("Student record updated.")


def display_all_students():
    """Display all student records."""
    rows = read_csv(STUDENT_FILE)
    if not rows:
        print("No student records found.")
        return
    print(f"\n{'─'*60}")
    for i, row in enumerate(rows, 1):
        print(f"\nRecord #{i}")
        s = Student(**row)
        s.display_records()
    print(f"{'─'*60}")


def search_student():
    """Search for a student by email and print time taken."""
    import time
    email = input("Enter student email to search: ").strip()
    rows = read_csv(STUDENT_FILE)

    start = time.time()
    found = None
    for row in rows:
        if row["email"] == email:
            found = row
            break
    end = time.time()

    if found:
        print("\nStudent found:")
        Student(**found).display_records()
    else:
        print("Student not found.")

    print(f"Search time: {(end - start) * 1000:.4f} ms")


def sort_students():
    """Sort and display students by name or marks."""
    print("\nSort by:")
    print("1. Email (ascending)")
    print("2. Email (descending)")
    print("3. Marks (ascending)")
    print("4. Marks (descending)")
    choice = input("Enter choice: ").strip()

    import time
    rows = read_csv(STUDENT_FILE)
    start = time.time()

    if choice == "1":
        rows.sort(key=lambda r: r["email"])
    elif choice == "2":
        rows.sort(key=lambda r: r["email"], reverse=True)
    elif choice == "3":
        rows.sort(key=lambda r: float(r["marks"]))
    elif choice == "4":
        rows.sort(key=lambda r: float(r["marks"]), reverse=True)
    else:
        print("Invalid choice.")
        return

    end = time.time()
    print(f"\nSorted results ({(end - start) * 1000:.4f} ms):")
    print(f"{'─'*60}")
    for i, row in enumerate(rows, 1):
        print(f"  {i}. {row['email']}  |  {row['first_name']} {row['last_name']}  |  Marks: {row['marks']}  |  Grade: {row['grade']}")


def check_my_grades(email):
    """Show grades for a specific student (used for student login)."""
    rows = read_csv(STUDENT_FILE)
    found = False
    for row in rows:
        if row["email"] == email:
            found = True
            print(f"\nCourse: {row['course_id']}  |  Grade: {row['grade']}  |  Marks: {row['marks']}")
    if not found:
        print("No grade records found for your account.")


def course_statistics():
    """Calculate average and median marks for a course."""
    course_id = input("Enter course ID: ").strip()
    rows = read_csv(STUDENT_FILE)
    marks_list = []

    for row in rows:
        if row["course_id"] == course_id:
            try:
                marks_list.append(float(row["marks"]))
            except ValueError:
                pass

    if not marks_list:
        print(f"No student records found for course {course_id}.")
        return

    average = sum(marks_list) / len(marks_list)
    sorted_marks = sorted(marks_list)
    n = len(sorted_marks)
    if n % 2 == 0:
        median = (sorted_marks[n // 2 - 1] + sorted_marks[n // 2]) / 2
    else:
        median = sorted_marks[n // 2]

    print(f"\nCourse: {course_id}")
    print(f"  Number of students : {n}")
    print(f"  Average marks      : {average:.2f}")
    print(f"  Median marks       : {median:.2f}")
