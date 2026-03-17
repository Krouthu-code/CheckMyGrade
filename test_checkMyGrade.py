"""
test_checkMyGrade.py
Unit tests for CheckMyGrade application.
Run with: python test_checkMyGrade.py
"""

import unittest
import os
import time
import random
import string

from csv_helper import read_csv, write_csv, append_csv
from student import (
    STUDENT_FILE, STUDENT_FIELDS, get_letter_grade, Student
)
from course import COURSE_FILE, COURSE_FIELDS, Course
from professor import PROFESSOR_FILE, PROFESSOR_FIELDS, Professor
from encryption import encrypt_password, decrypt_password


# ─── Helper Functions ─────────────────────────────────────────────────────────

def random_email():
    """Generate a random email address."""
    letters = string.ascii_lowercase
    name = "".join(random.choices(letters, k=6))
    return f"{name}@test.edu"


def seed_students(count=1000):
    """Add `count` student records to the CSV file for testing."""
    courses = ["DATA200", "CS101", "MATH300", "ENG150"]
    rows = []
    emails_used = set()

    for _ in range(count):
        email = random_email()
        while email in emails_used:
            email = random_email()
        emails_used.add(email)

        marks = round(random.uniform(50, 100), 1)
        grade = get_letter_grade(marks)
        rows.append({
            "email": email,
            "first_name": "Test",
            "last_name": "User",
            "course_id": random.choice(courses),
            "grade": grade,
            "marks": marks,
        })
    write_csv(STUDENT_FILE, rows, STUDENT_FIELDS)
    return rows


# ─── Test Classes ─────────────────────────────────────────────────────────────

class TestEncryption(unittest.TestCase):
    """Test password encryption and decryption."""

    def test_encrypt_decrypt(self):
        original = "Welcome12#_"
        encrypted = encrypt_password(original)
        self.assertNotEqual(original, encrypted)
        decrypted = decrypt_password(encrypted)
        self.assertEqual(original, decrypted)

    def test_encrypted_is_string(self):
        result = encrypt_password("hello123")
        self.assertIsInstance(result, str)


class TestStudentRecords(unittest.TestCase):
    """Test adding, deleting, and modifying student records."""

    def setUp(self):
        """Start each test with a clean student file."""
        write_csv(STUDENT_FILE, [], STUDENT_FIELDS)

    def test_add_student(self):
        row = {
            "email": "alice@test.edu",
            "first_name": "Alice",
            "last_name": "Smith",
            "course_id": "DATA200",
            "grade": "A",
            "marks": "95",
        }
        append_csv(STUDENT_FILE, row, STUDENT_FIELDS)
        rows = read_csv(STUDENT_FILE)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["email"], "alice@test.edu")

    def test_delete_student(self):
        row = {
            "email": "bob@test.edu",
            "first_name": "Bob",
            "last_name": "Jones",
            "course_id": "CS101",
            "grade": "B",
            "marks": "82",
        }
        append_csv(STUDENT_FILE, row, STUDENT_FIELDS)
        rows = read_csv(STUDENT_FILE)
        rows = [r for r in rows if r["email"] != "bob@test.edu"]
        write_csv(STUDENT_FILE, rows, STUDENT_FIELDS)
        self.assertEqual(len(read_csv(STUDENT_FILE)), 0)

    def test_modify_student_marks(self):
        row = {
            "email": "carol@test.edu",
            "first_name": "Carol",
            "last_name": "King",
            "course_id": "MATH300",
            "grade": "C",
            "marks": "72",
        }
        append_csv(STUDENT_FILE, row, STUDENT_FIELDS)
        rows = read_csv(STUDENT_FILE)
        for r in rows:
            if r["email"] == "carol@test.edu":
                r["marks"] = "88"
                r["grade"] = get_letter_grade(88)
        write_csv(STUDENT_FILE, rows, STUDENT_FIELDS)
        rows = read_csv(STUDENT_FILE)
        self.assertEqual(rows[0]["marks"], "88")
        self.assertEqual(rows[0]["grade"], "B")

    def test_1000_records_add(self):
        """Add 1000 student records and verify count."""
        rows = seed_students(1000)
        self.assertEqual(len(read_csv(STUDENT_FILE)), 1000)
        print(f"\n  [PASS] 1000 student records added.")


class TestSearchAndSort(unittest.TestCase):
    """Test searching and sorting student records."""

    @classmethod
    def setUpClass(cls):
        """Seed 1000 records once before all tests in this class."""
        cls.seeded_rows = seed_students(1000)
        cls.target_email = cls.seeded_rows[500]["email"]

    def test_search_student(self):
        rows = read_csv(STUDENT_FILE)
        start = time.time()
        found = None
        for row in rows:
            if row["email"] == self.target_email:
                found = row
                break
        elapsed = (time.time() - start) * 1000
        self.assertIsNotNone(found)
        print(f"\n  [PASS] Search completed in {elapsed:.4f} ms")

    def test_sort_by_email_ascending(self):
        rows = read_csv(STUDENT_FILE)
        start = time.time()
        sorted_rows = sorted(rows, key=lambda r: r["email"])
        elapsed = (time.time() - start) * 1000
        # Verify it's sorted
        emails = [r["email"] for r in sorted_rows]
        self.assertEqual(emails, sorted(emails))
        print(f"\n  [PASS] Sort by email ASC in {elapsed:.4f} ms")

    def test_sort_by_marks_descending(self):
        rows = read_csv(STUDENT_FILE)
        start = time.time()
        sorted_rows = sorted(rows, key=lambda r: float(r["marks"]), reverse=True)
        elapsed = (time.time() - start) * 1000
        marks = [float(r["marks"]) for r in sorted_rows]
        self.assertEqual(marks, sorted(marks, reverse=True))
        print(f"\n  [PASS] Sort by marks DESC in {elapsed:.4f} ms")


class TestCourseOperations(unittest.TestCase):
    """Test adding, deleting, and modifying course records."""

    def setUp(self):
        write_csv(COURSE_FILE, [], COURSE_FIELDS)

    def test_add_course(self):
        row = {"course_id": "CS101", "course_name": "Intro to CS", "description": "Basics", "credits": "3"}
        append_csv(COURSE_FILE, row, COURSE_FIELDS)
        rows = read_csv(COURSE_FILE)
        self.assertEqual(rows[0]["course_id"], "CS101")

    def test_delete_course(self):
        row = {"course_id": "MATH300", "course_name": "Calculus", "description": "Math", "credits": "4"}
        append_csv(COURSE_FILE, row, COURSE_FIELDS)
        rows = read_csv(COURSE_FILE)
        rows = [r for r in rows if r["course_id"] != "MATH300"]
        write_csv(COURSE_FILE, rows, COURSE_FIELDS)
        self.assertEqual(len(read_csv(COURSE_FILE)), 0)

    def test_modify_course(self):
        row = {"course_id": "ENG150", "course_name": "English", "description": "Writing", "credits": "3"}
        append_csv(COURSE_FILE, row, COURSE_FIELDS)
        rows = read_csv(COURSE_FILE)
        for r in rows:
            if r["course_id"] == "ENG150":
                r["course_name"] = "Advanced English"
        write_csv(COURSE_FILE, rows, COURSE_FIELDS)
        rows = read_csv(COURSE_FILE)
        self.assertEqual(rows[0]["course_name"], "Advanced English")


class TestProfessorOperations(unittest.TestCase):
    """Test adding, deleting, and modifying professor records."""

    def setUp(self):
        write_csv(PROFESSOR_FILE, [], PROFESSOR_FIELDS)

    def test_add_professor(self):
        row = {"email": "prof@test.edu", "name": "Dr. Smith", "rank": "Senior Professor", "course_id": "CS101"}
        append_csv(PROFESSOR_FILE, row, PROFESSOR_FIELDS)
        rows = read_csv(PROFESSOR_FILE)
        self.assertEqual(rows[0]["email"], "prof@test.edu")

    def test_delete_professor(self):
        row = {"email": "prof2@test.edu", "name": "Dr. Lee", "rank": "Junior Professor", "course_id": "DATA200"}
        append_csv(PROFESSOR_FILE, row, PROFESSOR_FIELDS)
        rows = [r for r in read_csv(PROFESSOR_FILE) if r["email"] != "prof2@test.edu"]
        write_csv(PROFESSOR_FILE, rows, PROFESSOR_FIELDS)
        self.assertEqual(len(read_csv(PROFESSOR_FILE)), 0)

    def test_modify_professor(self):
        row = {"email": "prof3@test.edu", "name": "Dr. Brown", "rank": "Junior Professor", "course_id": "MATH300"}
        append_csv(PROFESSOR_FILE, row, PROFESSOR_FIELDS)
        rows = read_csv(PROFESSOR_FILE)
        for r in rows:
            if r["email"] == "prof3@test.edu":
                r["rank"] = "Senior Professor"
        write_csv(PROFESSOR_FILE, rows, PROFESSOR_FIELDS)
        rows = read_csv(PROFESSOR_FILE)
        self.assertEqual(rows[0]["rank"], "Senior Professor")


class TestGradeScale(unittest.TestCase):
    """Test the grade-letter assignment logic."""

    def test_grade_A(self):
        self.assertEqual(get_letter_grade(95), "A")

    def test_grade_B(self):
        self.assertEqual(get_letter_grade(85), "B")

    def test_grade_C(self):
        self.assertEqual(get_letter_grade(75), "C")

    def test_grade_D(self):
        self.assertEqual(get_letter_grade(65), "D")

    def test_grade_F(self):
        self.assertEqual(get_letter_grade(50), "F")


if __name__ == "__main__":
    unittest.main(verbosity=2)
