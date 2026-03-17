"""
course.py
Course class with all course-related operations.
Courses are stored in courses.csv
"""

from csv_helper import read_csv, write_csv, append_csv

COURSE_FILE = "courses.csv"
COURSE_FIELDS = ["course_id", "course_name", "description", "credits"]


class Course:
    def __init__(self, course_id, course_name, description, credits):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.credits = credits

    def display_courses(self):
        """Print this course's details."""
        print(f"  Course ID   : {self.course_id}")
        print(f"  Name        : {self.course_name}")
        print(f"  Description : {self.description}")
        print(f"  Credits     : {self.credits}")

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "description": self.description,
            "credits": self.credits,
        }


# ─── CRUD Operations ─────────────────────────────────────────────────────────

def add_new_course():
    """Add a new course."""
    course_id = input("Course ID: ").strip()
    if not course_id:
        print("Course ID cannot be empty.")
        return

    rows = read_csv(COURSE_FILE)
    for row in rows:
        if row["course_id"] == course_id:
            print("A course with this ID already exists.")
            return

    course_name = input("Course name: ").strip()
    description = input("Description: ").strip()
    credits = input("Credits: ").strip()

    course = Course(course_id, course_name, description, credits)
    append_csv(COURSE_FILE, course.to_dict(), COURSE_FIELDS)
    print(f"Course '{course_name}' added successfully!")


def delete_course():
    """Delete a course by ID."""
    course_id = input("Enter course ID to delete: ").strip()
    rows = read_csv(COURSE_FILE)
    new_rows = [row for row in rows if row["course_id"] != course_id]

    if len(new_rows) == len(rows):
        print("Course not found.")
    else:
        write_csv(COURSE_FILE, new_rows, COURSE_FIELDS)
        print("Course deleted.")


def modify_course():
    """Modify a course's name or description."""
    course_id = input("Enter course ID to modify: ").strip()
    rows = read_csv(COURSE_FILE)
    found = False

    for row in rows:
        if row["course_id"] == course_id:
            found = True
            print(f"Current name: {row['course_name']}")
            new_name = input("New name (press Enter to keep): ").strip()
            if new_name:
                row["course_name"] = new_name

            print(f"Current description: {row['description']}")
            new_desc = input("New description (press Enter to keep): ").strip()
            if new_desc:
                row["description"] = new_desc
            break

    if not found:
        print("Course not found.")
    else:
        write_csv(COURSE_FILE, rows, COURSE_FIELDS)
        print("Course updated.")


def display_all_courses():
    """Display all courses."""
    rows = read_csv(COURSE_FILE)
    if not rows:
        print("No courses found.")
        return
    print(f"\n{'─'*50}")
    for i, row in enumerate(rows, 1):
        print(f"\nCourse #{i}")
        Course(**row).display_courses()
    print(f"{'─'*50}")
