"""
Test cases for the Attendance Management System module.
Run with:  python -m unittest test_attendance.py -v
"""

import unittest
from functions import attendance_percentage, attendance_status


class TestAttendanceSimpleCases(unittest.TestCase):
    """12 simple test cases for core attendance functionality."""

    def test_perfect_attendance(self):
        """100% attendance when all days are present."""
        self.assertEqual(attendance_percentage(30, 30), 100.0)

    def test_half_attendance(self):
        """50% attendance when half the days are present."""
        self.assertEqual(attendance_percentage(50, 100), 50.0)

    def test_zero_attendance(self):
        """0% attendance when no days are present."""
        self.assertEqual(attendance_percentage(0, 30), 0.0)

    def test_threshold_eligible_75(self):
        """Exactly 75% attendance should be Eligible."""
        self.assertEqual(attendance_percentage(75, 100), 75.0)

    def test_status_eligible_at_100(self):
        """100% status is Eligible."""
        self.assertEqual(attendance_status(100.0), "Eligible")

    def test_status_eligible_at_75(self):
        """75% status is Eligible (boundary)."""
        self.assertEqual(attendance_status(75.0), "Eligible")

    def test_status_warning_at_74(self):
        """74% status is Warning."""
        self.assertEqual(attendance_status(74.0), "Warning")

    def test_status_warning_at_60(self):
        """60% status is Warning (boundary)."""
        self.assertEqual(attendance_status(60.0), "Warning")

    def test_status_shortage_at_59(self):
        """59% status is Shortage."""
        self.assertEqual(attendance_status(59.0), "Shortage")

    def test_status_shortage_at_zero(self):
        """0% status is Shortage."""
        self.assertEqual(attendance_status(0.0), "Shortage")

    def test_single_day_present(self):
        """1 day present out of 1 day is 100%."""
        self.assertEqual(attendance_percentage(1, 1), 100.0)

    def test_attendance_record_fields(self):
        """Verify an attendance record dictionary has all required keys."""
        record = {
            "name": "John Doe",
            "id": "S101",
            "total_days": 30,
            "present": 24,
            "percentage": attendance_percentage(24, 30),
        }
        record["status"] = attendance_status(record["percentage"])
        self.assertIn("name", record)
        self.assertIn("id", record)
        self.assertIn("total_days", record)
        self.assertIn("present", record)
        self.assertIn("percentage", record)
        self.assertIn("status", record)


class TestAttendanceEdgeCases(unittest.TestCase):
    """8 edge case test cases for attendance functionality."""

    def test_zero_total_days_division_by_zero(self):
        """Division by zero when total_days is 0 should raise ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            attendance_percentage(5, 0)

    def test_present_greater_than_total_days(self):
        """Present days exceeding total days yields percentage > 100."""
        self.assertEqual(attendance_percentage(35, 30), 116.66666666666667)

    def test_negative_present_days(self):
        """Negative present days yield negative percentage."""
        self.assertAlmostEqual(attendance_percentage(-5, 30), -16.666666666666668)

    def test_negative_total_days(self):
        """Negative total days yield negative percentage."""
        self.assertEqual(attendance_percentage(10, -5), -200.0)

    def test_status_negative_percentage(self):
        """Negative percentage status is Shortage."""
        self.assertEqual(attendance_status(-10.0), "Shortage")

    def test_status_above_100_percentage(self):
        """Percentage above 100 is still Eligible."""
        self.assertEqual(attendance_status(150.0), "Eligible")

    def test_floating_point_attendance(self):
        """Floating point inputs produce correct floating percentage."""
        result = attendance_percentage(7, 3)
        self.assertAlmostEqual(result, 233.3333333333333, places=6)

    def test_exact_75_boundary_eligibility(self):
        """Exactly 75.0% is the boundary for Eligible status."""
        self.assertEqual(attendance_status(75.0), "Eligible")
        self.assertEqual(attendance_status(74.999), "Warning")


if __name__ == "__main__":
    unittest.main()