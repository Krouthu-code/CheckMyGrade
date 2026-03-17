"""
csv_helper.py
Helper functions to read and write CSV files easily.
"""

import csv
import os


def read_csv(filename):
    """Read a CSV file and return a list of dictionaries."""
    rows = []
    if not os.path.exists(filename):
        return rows  # Return empty list if file doesn't exist
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows


def write_csv(filename, rows, fieldnames):
    """Write a list of dictionaries to a CSV file."""
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_csv(filename, row, fieldnames):
    """Append a single row (dictionary) to a CSV file."""
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()  # Write header only if file is new
        writer.writerow(row)
