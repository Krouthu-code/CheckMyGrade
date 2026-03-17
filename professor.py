"""
professor.py
Professor class with all professor-related operations.
Professors are stored in professors.csv
"""

from csv_helper import read_csv, write_csv, append_csv

PROFESSOR_FILE = "professors.csv"
PROFESSOR_FIELDS = ["email", "name", "rank", "course_id"]


class Professor:
    def __init__(self, email, name, rank, course_id):
        self.email = email
        self.name = name
        self.rank = rank
        self.course_id = course_id

    def professors_details(self):
        """Print this professor's details."""
        print(f"  Email     : {self.email}")
        print(f"  Name      : {self.name}")
        print(f"  Rank      : {self.rank}")
        print(f"  Course ID : {self.course_id}")

    def to_dict(self):
        return {
            "email": self.email,
            "name": self.name,
            "rank": self.rank,
            "course_id": self.course_id,
        }


# ─── CRUD Operations ─────────────────────────────────────────────────────────

def add_new_professor():
    """Add a new professor."""
    email = input("Professor email: ").strip()
    if not email:
        print("Email cannot be empty.")
        return

    rows = read_csv(PROFESSOR_FILE)
    for row in rows:
        if row["email"] == email:
            print("A professor with this email already exists.")
            return

    name = input("Professor name: ").strip()
    rank = input("Rank (e.g. Junior/Senior Professor): ").strip()
    course_id = input("Course ID: ").strip()

    professor = Professor(email, name, rank, course_id)
    append_csv(PROFESSOR_FILE, professor.to_dict(), PROFESSOR_FIELDS)
    print(f"Professor '{name}' added successfully!")


def delete_professor():
    """Delete a professor by email."""
    email = input("Enter professor email to delete: ").strip()
    rows = read_csv(PROFESSOR_FILE)
    new_rows = [row for row in rows if row["email"] != email]

    if len(new_rows) == len(rows):
        print("Professor not found.")
    else:
        write_csv(PROFESSOR_FILE, new_rows, PROFESSOR_FIELDS)
        print("Professor deleted.")


def modify_professor():
    """Modify a professor's details."""
    email = input("Enter professor email to modify: ").strip()
    rows = read_csv(PROFESSOR_FILE)
    found = False

    for row in rows:
        if row["email"] == email:
            found = True
            print(f"Current name: {row['name']}")
            new_name = input("New name (press Enter to keep): ").strip()
            if new_name:
                row["name"] = new_name

            print(f"Current rank: {row['rank']}")
            new_rank = input("New rank (press Enter to keep): ").strip()
            if new_rank:
                row["rank"] = new_rank

            print(f"Current course ID: {row['course_id']}")
            new_course = input("New course ID (press Enter to keep): ").strip()
            if new_course:
                row["course_id"] = new_course
            break

    if not found:
        print("Professor not found.")
    else:
        write_csv(PROFESSOR_FILE, rows, PROFESSOR_FIELDS)
        print("Professor record updated.")


def display_all_professors():
    """Display all professors."""
    rows = read_csv(PROFESSOR_FILE)
    if not rows:
        print("No professors found.")
        return
    print(f"\n{'─'*50}")
    for i, row in enumerate(rows, 1):
        print(f"\nProfessor #{i}")
        Professor(**row).professors_details()
    print(f"{'─'*50}")


def show_course_details_by_professor():
    """Show all students in the courses taught by a professor."""
    from csv_helper import read_csv as _read
    email = input("Enter professor email: ").strip()

    prof_rows = read_csv(PROFESSOR_FILE)
    course_ids = [r["course_id"] for r in prof_rows if r["email"] == email]

    if not course_ids:
        print("Professor not found.")
        return

    student_rows = _read("students.csv")
    print(f"\nStudents for professor {email}:")
    print(f"{'─'*50}")
    for row in student_rows:
        if row["course_id"] in course_ids:
            print(f"  {row['email']}  |  {row['first_name']} {row['last_name']}  |  {row['course_id']}  |  Grade: {row['grade']}")
