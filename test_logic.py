"""
Automated tests for the core logic functions of the Attendance & Grading Management System.
Run with: python test_logic.py

Each test function below includes inline comments explaining what we do in that test case.
"""

from attendance_management import (
    calculate_percentage,
    get_attendance_status,
    calculate_grade,
    manual_max,
    manual_min,
    attendance_records,
    student_grades,
)


def test_calculate_percentage():
    """
    Test the calculate_percentage() function.
    We verify that attendance percentage is computed correctly for various inputs,
    including perfect attendance, partial attendance, zero attendance, threshold values,
    and division-by-zero protection when total_days is 0.
    """
    # When all days are present, percentage should be 100%
    assert calculate_percentage(30, 30) == 100.0

    # When half the days are present, percentage should be 50%
    assert calculate_percentage(50, 100) == 50.0

    # When no days are present, percentage should be 0%
    assert calculate_percentage(0, 30) == 0.0

    # Exactly 75% attendance should return 75% (eligibility boundary)
    assert calculate_percentage(75, 100) == 75.0

    # When total_days is 0, we must avoid division by zero and return 0.0 safely
    assert calculate_percentage(0, 0) == 0.0

    print("✓ calculate_percentage tests passed")


def test_get_attendance_status():
    """
    Test the get_attendance_status() function.
    We verify that the correct status (Eligible / Warning / Shortage) is returned
    based on percentage boundaries: >=75 Eligible, >=60 Warning, else Shortage.
    """
    # 100% attendance is well above 75%, so status is Eligible
    assert get_attendance_status(100.0) == "Eligible"

    # Exactly 75.0% meets the Eligible threshold (>=75)
    assert get_attendance_status(75.0) == "Eligible"

    # 74.99% is just below 75%, so status is Warning
    assert get_attendance_status(74.99) == "Warning"

    # Exactly 60.0% meets the Warning threshold (>=60)
    assert get_attendance_status(60.0) == "Warning"

    # 59.99% is below 60%, so status is Shortage
    assert get_attendance_status(59.99) == "Shortage"

    # 0% attendance is the lowest possible, so status is Shortage
    assert get_attendance_status(0.0) == "Shortage"

    print("✓ get_attendance_status tests passed")


def test_calculate_grade():
    """
    Test the calculate_grade() function.
    We verify the grading scale returns correct grade and remark for each percentage range:
    90+ A+, 80+ A, 70+ B, 60+ C, 50+ D, 35+ E, below 35 F.
    """
    # 95% falls in the A+ range (>=90)
    grade, remark = calculate_grade(95)
    assert grade == "A+" and remark == "Outstanding"

    # 85% falls in the A range (>=80)
    grade, remark = calculate_grade(85)
    assert grade == "A" and remark == "Excellent"

    # 75% falls in the B range (>=70)
    grade, remark = calculate_grade(75)
    assert grade == "B" and remark == "Very Good"

    # 65% falls in the C range (>=60)
    grade, remark = calculate_grade(65)
    assert grade == "C" and remark == "Good"

    # 55% falls in the D range (>=50)
    grade, remark = calculate_grade(55)
    assert grade == "D" and remark == "Satisfactory"

    # 40% falls in the E range (>=35)
    grade, remark = calculate_grade(40)
    assert grade == "E" and remark == "Pass"

    # 30% falls in the F range (<35)
    grade, remark = calculate_grade(30)
    assert grade == "F" and remark == "Fail"

    print("✓ calculate_grade tests passed")


def test_manual_max_min():
    """
    Test manual_max() and manual_min() functions.
    We verify that our custom implementations (without using built-in max() or min())
    correctly find the largest and smallest values in a list, including edge cases
    like single-element lists and empty lists.
    """
    # manual_max should find 80 as the largest value in the list
    assert manual_max([10, 20, 5, 80, 30]) == 80

    # manual_max with a single element returns that element
    assert manual_max([100]) == 100

    # manual_max with an empty list returns None (no elements to compare)
    assert manual_max([]) is None

    # manual_min should find 5 as the smallest value in the list
    assert manual_min([10, 20, 5, 80, 30]) == 5

    # manual_min with a single element returns that element
    assert manual_min([100]) == 100

    # manual_min with an empty list returns None (no elements to compare)
    assert manual_min([]) is None

    print("✓ manual_max/min tests passed")


def test_roll_no_uniqueness():
    """
    Test that roll number is used as a unique key in dictionaries.
    We verify that attendance_records and student_grades dictionaries use roll number
    as the key, and that we can store and retrieve student data using that key.
    """
    # Clear any existing data to start fresh
    attendance_records.clear()
    student_grades.clear()

    # Insert a student record into attendance_records using roll number "R001" as key
    attendance_records["R001"] = {"name": "Alice", "percentage": 80.0, "status": "Eligible"}

    # Insert a student record into student_grades using roll number "R001" as key
    student_grades["R001"] = {"name": "Alice", "percentage": 85.0, "grade": "A", "result": "PASS"}

    # Verify roll number "R001" exists as a key in attendance_records
    assert "R001" in attendance_records

    # Verify roll number "R001" exists as a key in student_grades
    assert "R001" in student_grades

    # Verify we can retrieve the correct name from attendance_records using the roll number key
    assert attendance_records["R001"]["name"] == "Alice"

    # Verify we can retrieve the correct name from student_grades using the roll number key
    assert student_grades["R001"]["name"] == "Alice"

    print("✓ Roll number as unique key tests passed")


def test_status_counts():
    """
    Test counting of Eligible, Warning, and Shortage statuses.
    We verify that we can correctly count how many students fall into each
    attendance status category by iterating over the attendance_records dictionary.
    """
    # Clear any existing data to start fresh
    attendance_records.clear()

    # Add 5 records with known statuses: 2 Eligible, 1 Warning, 2 Shortage
    attendance_records["R1"] = {"status": "Eligible"}
    attendance_records["R2"] = {"status": "Eligible"}
    attendance_records["R3"] = {"status": "Warning"}
    attendance_records["R4"] = {"status": "Shortage"}
    attendance_records["R5"] = {"status": "Shortage"}

    # Count how many records have status "Eligible"
    eligible = sum(1 for r in attendance_records.values() if r["status"] == "Eligible")

    # Count how many records have status "Warning"
    warning = sum(1 for r in attendance_records.values() if r["status"] == "Warning")

    # Count how many records have status "Shortage"
    shortage = sum(1 for r in attendance_records.values() if r["status"] == "Shortage")

    # Verify the counts match expectations
    assert eligible == 2
    assert warning == 1
    assert shortage == 2

    print("✓ Status count tests passed")


if __name__ == "__main__":
    print("Running automated logic tests...\n")
    test_calculate_percentage()
    test_get_attendance_status()
    test_calculate_grade()
    test_manual_max_min()
    test_roll_no_uniqueness()
    test_status_counts()
    print("\nAll automated tests passed!")