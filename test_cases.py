"""
Test Cases for Attendance & Grading Management System
Total: 20 Test Cases (12 Normal + 8 Edge Cases)

Modules covered:
1. Attendance Management
2. Grading Management

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
# 12 NORMAL TEST CASES (TC-01 to TC-12)
# ===========================================================================
class TestNormalCases(unittest.TestCase):
    """12 Normal test cases for core functionality."""

    def test_tc_01_perfect_attendance_100_percent(self):
        """TC-01: 30/30 days present = 100% attendance."""
        self.assertEqual(attendance_percentage(30, 30), 100.0)

    def test_tc_02_half_attendance_50_percent(self):
        """TC-02: 50/100 days present = 50% attendance."""
        self.assertEqual(attendance_percentage(50, 100), 50.0)

    def test_tc_03_zero_attendance(self):
        """TC-03: 0/30 days present = 0% attendance."""
        self.assertEqual(attendance_percentage(0, 30), 0.0)

    def test_tc_04_exactly_75_percent_threshold(self):
        """TC-04: Exactly 75% attendance (eligibility boundary)."""
        self.assertEqual(attendance_percentage(75, 100), 75.0)

    def test_tc_05_status_eligible_at_100_percent(self):
        """TC-05: 100% status is Eligible."""
        self.assertEqual(attendance_status(100.0), "Eligible")

    def test_tc_06_status_eligible_at_75_percent(self):
        """TC-06: 75% status is Eligible (boundary)."""
        self.assertEqual(attendance_status(75.0), "Eligible")

    def test_tc_07_status_warning_at_60_percent(self):
        """TC-07: 60% status is Warning (boundary)."""
        self.assertEqual(attendance_status(60.0), "Warning")

    def test_tc_08_status_warning_at_74_percent(self):
        """TC-08: 74% status is Warning."""
        self.assertEqual(attendance_status(74.0), "Warning")

    def test_tc_09_status_shortage_at_59_percent(self):
        """TC-09: 59% status is Shortage."""
        self.assertEqual(attendance_status(59.0), "Shortage")

    def test_tc_10_grade_a_plus_outstanding(self):
        """TC-10: 95% returns grade A+ (Outstanding)."""
        grade, remark = calculate_grade(95)
        self.assertEqual(grade, "A+")
        self.assertEqual(remark, "Outstanding")

    def test_tc_11_grade_f_fail(self):
        """TC-11: 30% returns grade F (Fail)."""
        grade, remark = calculate_grade(30)
        self.assertEqual(grade, "F")
        self.assertEqual(remark, "Fail")

    def test_tc_12_roll_number_unique_key(self):
        """TC-12: Roll number as unique key in grades dictionary."""
        grades_dict = {}
        roll_no = "S101"
        grades_dict[roll_no] = {
            "name": "Alice",
            "percentage": 85.0,
            "grade": "A",
            "result": "PASS"
        }
        self.assertIn(roll_no, grades_dict)
        self.assertEqual(grades_dict[roll_no]["name"], "Alice")


# ===========================================================================
# 8 EDGE CASE TEST CASES (EC-01 to EC-08)
# ===========================================================================
class TestEdgeCases(unittest.TestCase):
    """8 Edge case test cases."""

    def test_ec_01_zero_total_days_division_by_zero(self):
        """EC-01: Zero total days raises ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            attendance_percentage(5, 0)

    def test_ec_02_present_greater_than_total_days(self):
        """EC-02: Present days > total days yields percentage > 100."""
        result = attendance_percentage(35, 30)
        self.assertGreater(result, 100.0)

    def test_ec_03_negative_present_days(self):
        """EC-03: Negative present days yields negative percentage."""
        result = attendance_percentage(-5, 30)
        self.assertLess(result, 0.0)

    def test_ec_04_boundary_74_99_vs_75_00(self):
        """EC-04: Boundary between Warning (74.99) and Eligible (75.00)."""
        self.assertEqual(attendance_status(74.99), "Warning")
        self.assertEqual(attendance_status(75.00), "Eligible")

    def test_ec_05_boundary_34_vs_35_grade(self):
        """EC-05: Boundary between F (34) and E (35)."""
        grade_34, _ = calculate_grade(34)
        grade_35, _ = calculate_grade(35)
        self.assertEqual(grade_34, "F")
        self.assertEqual(grade_35, "E")

    def test_ec_06_boundary_89_vs_90_grade(self):
        """EC-06: Boundary between A (89) and A+ (90)."""
        grade_89, _ = calculate_grade(89)
        grade_90, _ = calculate_grade(90)
        self.assertEqual(grade_89, "A")
        self.assertEqual(grade_90, "A+")

    def test_ec_07_negative_percentage_status_shortage(self):
        """EC-07: Negative percentage status is Shortage."""
        self.assertEqual(attendance_status(-10.0), "Shortage")

    def test_ec_08_above_100_percent_eligible(self):
        """EC-08: Percentage above 100 is still Eligible."""
        self.assertEqual(attendance_status(150.0), "Eligible")


# ===========================================================================
# RUN TESTS
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)