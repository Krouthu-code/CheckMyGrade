"""
grades.py
Grade management and report generation.
"""

from csv_helper import read_csv


GRADE_SCALE = [
    ("A", 90, 100),
    ("B", 80, 89),
    ("C", 70, 79),
    ("D", 60, 69),
    ("F",  0, 59),
]


class Grades:
    def __init__(self, grade_id, grade, marks_min, marks_max):
        self.grade_id = grade_id
        self.grade = grade
        self.marks_min = marks_min
        self.marks_max = marks_max

    def display_grade_report(self):
        print(f"  Grade: {self.grade}  |  Range: {self.marks_min} - {self.marks_max}")


def display_grade_scale():
    """Show the full grade scale."""
    print("\nGrade Scale:")
    print(f"{'─'*30}")
    for i, (grade, low, high) in enumerate(GRADE_SCALE, 1):
        g = Grades(i, grade, low, high)
        g.display_grade_report()


# ─── Report Functions ─────────────────────────────────────────────────────────

def report_by_course():
    """Display grade report grouped by course."""
    course_id = input("Enter course ID: ").strip()
    rows = read_csv("students.csv")

    print(f"\nGrade Report for Course: {course_id}")
    print(f"{'─'*50}")
    found = False
    for row in rows:
        if row["course_id"] == course_id:
            found = True
            print(f"  {row['email']}  |  {row['first_name']} {row['last_name']}  |  Grade: {row['grade']}  |  Marks: {row['marks']}")
    if not found:
        print("No records found for this course.")


def report_by_student():
    """Display grade report for a specific student."""
    email = input("Enter student email: ").strip()
    rows = read_csv("students.csv")

    print(f"\nGrade Report for Student: {email}")
    print(f"{'─'*50}")
    found = False
    for row in rows:
        if row["email"] == email:
            found = True
            print(f"  Course: {row['course_id']}  |  Grade: {row['grade']}  |  Marks: {row['marks']}")
    if not found:
        print("No records found for this student.")


def report_by_professor():
    """Display grade report for all courses taught by a professor."""
    prof_email = input("Enter professor email: ").strip()
    prof_rows = read_csv("professors.csv")

    course_ids = [r["course_id"] for r in prof_rows if r["email"] == prof_email]
    if not course_ids:
        print("Professor not found.")
        return

    student_rows = read_csv("students.csv")
    print(f"\nGrade Report for Professor: {prof_email}")
    print(f"{'─'*50}")
    for course_id in course_ids:
        print(f"\n  Course: {course_id}")
        for row in student_rows:
            if row["course_id"] == course_id:
                print(f"    {row['email']}  |  {row['first_name']} {row['last_name']}  |  Grade: {row['grade']}  |  Marks: {row['marks']}")
