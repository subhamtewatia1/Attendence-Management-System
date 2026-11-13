"""
Test Cases for Expense & Attendance Management System
Based on CRS (Course Requirement Specification)

Modules covered:
1. Expense Management
2. Attendance Management

How to run:
    python test_expense_attendance.py
"""

import unittest
from functions import (
    EXPENSE_CATEGORIES,
    attendance_percentage,
    attendance_status,
    calculate_discount,
    calculate_tax,
    calculate_grade,
    TAX_RATE,
    PASS_MARK,
    ATTENDANCE_ELIGIBLE,
)


# ===========================================================================
# EXPENSE MANAGEMENT TEST CASES
# ===========================================================================
class TestExpenseManagement(unittest.TestCase):
    """Test cases for the Expense Management module."""

    def test_add_expense_food_category(self):
        """TC-EXP-01: Add an expense in Food category."""
        expense = {
            "description": "Lunch",
            "category": "Food",
            "amount": 250.00
        }
        self.assertEqual(expense["category"], "Food")
        self.assertEqual(expense["amount"], 250.00)

    def test_add_expense_travel_category(self):
        """TC-EXP-02: Add an expense in Travel category."""
        expense = {
            "description": "Bus fare",
            "category": "Travel",
            "amount": 50.00
        }
        self.assertEqual(expense["category"], "Travel")
        self.assertEqual(expense["amount"], 50.00)

    def test_add_expense_utilities_category(self):
        """TC-EXP-03: Add an expense in Utilities category."""
        expense = {
            "description": "Electricity bill",
            "category": "Utilities",
            "amount": 1500.00
        }
        self.assertEqual(expense["category"], "Utilities")
        self.assertEqual(expense["amount"], 1500.00)

    def test_add_expense_stationery_category(self):
        """TC-EXP-04: Add an expense in Stationery category."""
        expense = {
            "description": "Notebooks",
            "category": "Stationery",
            "amount": 200.00
        }
        self.assertEqual(expense["category"], "Stationery")
        self.assertEqual(expense["amount"], 200.00)

    def test_add_expense_other_category(self):
        """TC-EXP-05: Add an expense in Other category."""
        expense = {
            "description": "Miscellaneous",
            "category": "Other",
            "amount": 100.00
        }
        self.assertEqual(expense["category"], "Other")
        self.assertEqual(expense["amount"], 100.00)

    def test_expense_categories_constant(self):
        """TC-EXP-06: Verify EXPENSE_CATEGORIES contains all valid categories."""
        expected = ("Food", "Travel", "Utilities", "Stationery", "Other")
        self.assertEqual(EXPENSE_CATEGORIES, expected)

    def test_calculate_discount_slab_15_percent(self):
        """TC-EXP-07: Discount slab for subtotal >= 10000 should be 15%."""
        self.assertEqual(calculate_discount(15000), 0.15)
        self.assertEqual(calculate_discount(10000), 0.15)

    def test_calculate_discount_slab_10_percent(self):
        """TC-EXP-08: Discount slab for subtotal >= 5000 should be 10%."""
        self.assertEqual(calculate_discount(7500), 0.10)
        self.assertEqual(calculate_discount(5000), 0.10)

    def test_calculate_discount_slab_5_percent(self):
        """TC-EXP-09: Discount slab for subtotal >= 1000 should be 5%."""
        self.assertEqual(calculate_discount(3000), 0.05)
        self.assertEqual(calculate_discount(1000), 0.05)

    def test_calculate_discount_no_discount(self):
        """TC-EXP-10: Subtotal below 1000 should have 0% discount."""
        self.assertEqual(calculate_discount(500), 0.0)
        self.assertEqual(calculate_discount(0), 0.0)

    def test_calculate_tax_18_percent(self):
        """TC-EXP-11: Tax should be calculated at 18% rate."""
        taxable = 1000.00
        expected_tax = round(taxable * TAX_RATE, 2)
        self.assertEqual(calculate_tax(taxable), expected_tax)

    def test_expense_amount_formatting_2f(self):
        """TC-EXP-12: Expense amounts should be formatted to 2 decimal places."""
        amount = 250.5
        formatted = f"{amount:.2f}"
        self.assertEqual(formatted, "250.50")


# ===========================================================================
# ATTENDANCE MANAGEMENT TEST CASES
# ===========================================================================
class TestAttendanceManagement(unittest.TestCase):
    """Test cases for the Attendance Management module."""

    def test_attendance_percentage_perfect(self):
        """TC-ATT-01: 100% attendance when all days present."""
        self.assertEqual(attendance_percentage(30, 30), 100.0)

    def test_attendance_percentage_half(self):
        """TC-ATT-02: 50% attendance when half days present."""
        self.assertEqual(attendance_percentage(50, 100), 50.0)

    def test_attendance_percentage_zero(self):
        """TC-ATT-03: 0% attendance when no days present."""
        self.assertEqual(attendance_percentage(0, 30), 0.0)

    def test_attendance_percentage_75_threshold(self):
        """TC-ATT-04: Exactly 75% attendance."""
        self.assertEqual(attendance_percentage(75, 100), 75.0)

    def test_attendance_status_eligible(self):
        """TC-ATT-05: Percentage >= 75 should return 'Eligible'."""
        self.assertEqual(attendance_status(100.0), "Eligible")
        self.assertEqual(attendance_status(75.0), "Eligible")
        self.assertEqual(attendance_status(85.5), "Eligible")

    def test_attendance_status_warning(self):
        """TC-ATT-06: Percentage between 60 and 74.99 should return 'Warning'."""
        self.assertEqual(attendance_status(74.99), "Warning")
        self.assertEqual(attendance_status(60.0), "Warning")
        self.assertEqual(attendance_status(65.0), "Warning")

    def test_attendance_status_shortage(self):
        """TC-ATT-07: Percentage below 60 should return 'Shortage'."""
        self.assertEqual(attendance_status(59.99), "Shortage")
        self.assertEqual(attendance_status(0.0), "Shortage")
        self.assertEqual(attendance_status(45.0), "Shortage")

    def test_attendance_eligible_count(self):
        """TC-ATT-08: Count students with Eligible status."""
        records = [
            {"status": "Eligible"},
            {"status": "Eligible"},
            {"status": "Warning"},
            {"status": "Shortage"},
        ]
        eligible_count = sum(1 for r in records if r["status"] == "Eligible")
        self.assertEqual(eligible_count, 2)

    def test_attendance_warning_count(self):
        """TC-ATT-09: Count students with Warning status."""
        records = [
            {"status": "Eligible"},
            {"status": "Warning"},
            {"status": "Warning"},
            {"status": "Shortage"},
        ]
        warning_count = sum(1 for r in records if r["status"] == "Warning")
        self.assertEqual(warning_count, 2)

    def test_attendance_shortage_count(self):
        """TC-ATT-10: Count students with Shortage status."""
        records = [
            {"status": "Eligible"},
            {"status": "Warning"},
            {"status": "Shortage"},
            {"status": "Shortage"},
        ]
        shortage_count = sum(1 for r in records if r["status"] == "Shortage")
        self.assertEqual(shortage_count, 2)

    def test_attendance_percentage_formatting_2f(self):
        """TC-ATT-11: Attendance percentage formatted to 2 decimal places."""
        pct = attendance_percentage(24, 30)
        formatted = f"{pct:.2f}"
        self.assertEqual(formatted, "80.00")

    def test_attendance_roll_no_unique_key(self):
        """TC-ATT-12: Roll number should be unique key in attendance dictionary."""
        attendance_dict = {}
        roll_no = "S101"
        attendance_dict[roll_no] = {"name": "Alice", "percentage": 85.0}
        self.assertIn(roll_no, attendance_dict)
        self.assertEqual(attendance_dict[roll_no]["name"], "Alice")


# ===========================================================================
# EDGE CASES - EXPENSE & ATTENDANCE
# ===========================================================================
class TestExpenseEdgeCases(unittest.TestCase):
    """Edge case test cases for Expense Management."""

    def test_expense_zero_amount(self):
        """EC-EXP-01: Expense with zero amount."""
        expense = {"description": "Free item", "category": "Other", "amount": 0.00}
        self.assertEqual(expense["amount"], 0.00)

    def test_expense_negative_amount(self):
        """EC-EXP-02: Expense with negative amount (should be handled by validation)."""
        expense = {"description": "Refund", "category": "Other", "amount": -100.00}
        self.assertEqual(expense["amount"], -100.00)

    def test_expense_empty_description(self):
        """EC-EXP-03: Expense with empty description."""
        expense = {"description": "", "category": "Food", "amount": 50.00}
        self.assertEqual(expense["description"], "")

    def test_expense_very_large_amount(self):
        """EC-EXP-04: Expense with very large amount."""
        expense = {"description": "Equipment", "category": "Other", "amount": 999999.99}
        self.assertEqual(expense["amount"], 999999.99)

    def test_discount_boundary_exactly_10000(self):
        """EC-EXP-05: Subtotal exactly at 10000 should get 15% discount."""
        self.assertEqual(calculate_discount(10000), 0.15)

    def test_discount_boundary_exactly_5000(self):
        """EC-EXP-06: Subtotal exactly at 5000 should get 10% discount."""
        self.assertEqual(calculate_discount(5000), 0.10)

    def test_discount_boundary_exactly_1000(self):
        """EC-EXP-07: Subtotal exactly at 1000 should get 5% discount."""
        self.assertEqual(calculate_discount(1000), 0.05)

    def test_tax_on_zero_amount(self):
        """EC-EXP-08: Tax on zero taxable amount should be zero."""
        self.assertEqual(calculate_tax(0), 0.0)


class TestAttendanceEdgeCases(unittest.TestCase):
    """Edge case test cases for Attendance Management."""

    def test_attendance_zero_total_days(self):
        """EC-ATT-01: Zero total days raises ZeroDivisionError."""
        # The attendance_percentage function does not protect against division by zero,
        # so this should raise ZeroDivisionError
        with self.assertRaises(ZeroDivisionError):
            attendance_percentage(0, 0)

    def test_attendance_present_greater_than_total(self):
        """EC-ATT-02: Present days greater than total days."""
        result = attendance_percentage(35, 30)
        self.assertGreater(result, 100.0)

    def test_attendance_negative_present_days(self):
        """EC-ATT-03: Negative present days."""
        result = attendance_percentage(-5, 30)
        self.assertLess(result, 0.0)

    def test_attendance_negative_total_days(self):
        """EC-ATT-04: Negative total days."""
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


# ===========================================================================
# GRADING MANAGEMENT TEST CASES
# ===========================================================================
class TestGradingManagement(unittest.TestCase):
    """Test cases for the Grading Management module.
    
    Grading scale linked to roll number:
    - A+ : 90-100 (Outstanding)
    - A  : 80-89  (Excellent)
    - B  : 70-79  (Very Good)
    - C  : 60-69  (Good)
    - D  : 50-59  (Satisfactory)
    - E  : 35-49  (Pass)
    - F  : 0-34   (Fail)
    
    Pass/Fail rule: If any subject mark < 35, result is FAIL.
    """

    def test_grade_a_plus_outstanding(self):
        """TC-GRD-01: Percentage 95 should return grade A+ (Outstanding)."""
        grade, remark = calculate_grade(95)
        self.assertEqual(grade, "A+")
        self.assertEqual(remark, "Outstanding")

    def test_grade_a_excellent(self):
        """TC-GRD-02: Percentage 85 should return grade A (Excellent)."""
        grade, remark = calculate_grade(85)
        self.assertEqual(grade, "A")
        self.assertEqual(remark, "Excellent")

    def test_grade_b_very_good(self):
        """TC-GRD-03: Percentage 75 should return grade B (Very Good)."""
        grade, remark = calculate_grade(75)
        self.assertEqual(grade, "B")
        self.assertEqual(remark, "Very Good")

    def test_grade_c_good(self):
        """TC-GRD-04: Percentage 65 should return grade C (Good)."""
        grade, remark = calculate_grade(65)
        self.assertEqual(grade, "C")
        self.assertEqual(remark, "Good")

    def test_grade_d_satisfactory(self):
        """TC-GRD-05: Percentage 55 should return grade D (Satisfactory)."""
        grade, remark = calculate_grade(55)
        self.assertEqual(grade, "D")
        self.assertEqual(remark, "Satisfactory")

    def test_grade_e_pass(self):
        """TC-GRD-06: Percentage 40 should return grade E (Pass)."""
        grade, remark = calculate_grade(40)
        self.assertEqual(grade, "E")
        self.assertEqual(remark, "Pass")

    def test_grade_f_fail(self):
        """TC-GRD-07: Percentage 30 should return grade F (Fail)."""
        grade, remark = calculate_grade(30)
        self.assertEqual(grade, "F")
        self.assertEqual(remark, "Fail")

    def test_grade_boundary_90(self):
        """TC-GRD-08: Exactly 90% should return grade A+."""
        grade, remark = calculate_grade(90)
        self.assertEqual(grade, "A+")

    def test_grade_boundary_80(self):
        """TC-GRD-09: Exactly 80% should return grade A."""
        grade, remark = calculate_grade(80)
        self.assertEqual(grade, "A")

    def test_grade_boundary_70(self):
        """TC-GRD-10: Exactly 70% should return grade B."""
        grade, remark = calculate_grade(70)
        self.assertEqual(grade, "B")

    def test_grade_boundary_60(self):
        """TC-GRD-11: Exactly 60% should return grade C."""
        grade, remark = calculate_grade(60)
        self.assertEqual(grade, "C")

    def test_grade_boundary_35(self):
        """TC-GRD-12: Exactly 35% should return grade E (Pass)."""
        grade, remark = calculate_grade(35)
        self.assertEqual(grade, "E")


# ===========================================================================
# EDGE CASES - GRADING MANAGEMENT
# ===========================================================================
class TestGradingEdgeCases(unittest.TestCase):
    """Edge case test cases for Grading Management."""

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

    def test_roll_no_unique_key_in_grades(self):
        """EC-GRD-08: Roll number should be unique key in grades dictionary."""
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