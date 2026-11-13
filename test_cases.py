"""
Test Cases for Attendance & Grading Management System
20 Edge Cases Only (No Expense Management)

Modules covered:
1. Attendance Management - 10 Edge Cases
2. Grading Management - 10 Edge Cases

How to run:
    python test_cases.py
"""

import unittest
from functions import (
    attendance_percentage,
    attendance_status,
    calculate_grade,
)


# ===========================================================================
# ATTENDANCE MANAGEMENT - 10 EDGE CASES
# ===========================================================================
class TestAttendanceEdgeCases(unittest.TestCase):
    """10 Edge case test cases for Attendance Management."""

    def test_attendance_zero_total_days(self):
        """EC-ATT-01: Zero total days raises ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            attendance_percentage(0, 0)

    def test_attendance_present_greater_than_total(self):
        """EC-ATT-02: Present days greater than total days (>100%)."""
        result = attendance_percentage(35, 30)
        self.assertGreater(result, 100.0)

    def test_attendance_negative_present_days(self):
        """EC-ATT-03: Negative present days yields negative percentage."""
        result = attendance_percentage(-5, 30)
        self.assertLess(result, 0.0)

    def test_attendance_negative_total_days(self):
        """EC-ATT-04: Negative total days yields negative percentage."""
        result = attendance_percentage(10, -5)
        self.assertNotEqual(result, 0.0)

    def test_attendance_single_day(self):
        """EC-ATT-05: Single day present out of single total day."""
        self.assertEqual(attendance_percentage(1, 1), 100.0)

    def test_attendance_boundary_74_99_vs_75_00(self):
        """EC-ATT-06: Boundary between Warning (74.99) and Eligible (75.00)."""
        self.assertEqual(attendance_status(74.99), "Warning")
        self.assertEqual(attendance_status(75.00), "Eligible")

    def test_attendance_boundary_59_99_vs_60_00(self):
        """EC-ATT-07: Boundary between Shortage (59.99) and Warning (60.00)."""
        self.assertEqual(attendance_status(59.99), "Shortage")
        self.assertEqual(attendance_status(60.00), "Warning")

    def test_attendance_floating_point_input(self):
        """EC-ATT-08: Floating point input for present and total days."""
        result = attendance_percentage(7.5, 3.0)
        self.assertAlmostEqual(result, 250.0)

    def test_attendance_negative_percentage_status(self):
        """EC-ATT-09: Negative percentage status is Shortage."""
        self.assertEqual(attendance_status(-10.0), "Shortage")

    def test_attendance_above_100_percentage_status(self):
        """EC-ATT-10: Percentage above 100 is still Eligible."""
        self.assertEqual(attendance_status(150.0), "Eligible")


# ===========================================================================
# GRADING MANAGEMENT - 10 EDGE CASES
# ===========================================================================
class TestGradingEdgeCases(unittest.TestCase):
    """10 Edge case test cases for Grading Management."""

    def test_grade_100_percent(self):
        """EC-GRD-01: 100% should return grade A+."""
        grade, remark = calculate_grade(100)
        self.assertEqual(grade, "A+")
        self.assertEqual(remark, "Outstanding")

    def test_grade_zero_percent(self):
        """EC-GRD-02: 0% should return grade F (Fail)."""
        grade, remark = calculate_grade(0)
        self.assertEqual(grade, "F")
        self.assertEqual(remark, "Fail")

    def test_grade_negative_percentage(self):
        """EC-GRD-03: Negative percentage should return grade F."""
        grade, remark = calculate_grade(-10)
        self.assertEqual(grade, "F")
        self.assertEqual(remark, "Fail")

    def test_grade_above_100(self):
        """EC-GRD-04: Percentage above 100 should return grade A+."""
        grade, remark = calculate_grade(150)
        self.assertEqual(grade, "A+")
        self.assertEqual(remark, "Outstanding")

    def test_grade_boundary_89_vs_90(self):
        """EC-GRD-05: Boundary between A (89) and A+ (90)."""
        grade_89, _ = calculate_grade(89)
        grade_90, _ = calculate_grade(90)
        self.assertEqual(grade_89, "A")
        self.assertEqual(grade_90, "A+")

    def test_grade_boundary_34_vs_35(self):
        """EC-GRD-06: Boundary between F (34) and E (35)."""
        grade_34, _ = calculate_grade(34)
        grade_35, _ = calculate_grade(35)
        self.assertEqual(grade_34, "F")
        self.assertEqual(grade_35, "E")

    def test_grade_floating_point_percentage(self):
        """EC-GRD-07: Floating point percentage should return correct grade."""
        grade, remark = calculate_grade(85.5)
        self.assertEqual(grade, "A")
        self.assertEqual(remark, "Excellent")

    def test_grade_boundary_79_vs_80(self):
        """EC-GRD-08: Boundary between B (79) and A (80)."""
        grade_79, _ = calculate_grade(79)
        grade_80, _ = calculate_grade(80)
        self.assertEqual(grade_79, "B")
        self.assertEqual(grade_80, "A")

    def test_grade_boundary_49_vs_50(self):
        """EC-GRD-09: Boundary between D (49) and E (50)."""
        grade_49, _ = calculate_grade(49)
        grade_50, _ = calculate_grade(50)
        self.assertEqual(grade_49, "E")
        self.assertEqual(grade_50, "D")

    def test_grade_roll_no_unique_key(self):
        """EC-GRD-10: Roll number should be unique key in grades dictionary."""
        grades_dict = {}
        roll_no = "G101"
        grades_dict[roll_no] = {"name": "Bob", "percentage": 88.0, "grade": "A", "result": "PASS"}
        self.assertIn(roll_no, grades_dict)
        self.assertEqual(grades_dict[roll_no]["name"], "Bob")
        self.assertEqual(grades_dict[roll_no]["grade"], "A")


# ===========================================================================
# RUN TESTS
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)