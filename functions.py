"""
functions.py - Shared helper functions for Expense & Attendance Management System

Constraints followed:
- Uses ival() for input validation
- Uses map() for input processing
- CLI based (no GUI)
- .2f formatting for all decimal output
- Does NOT use eval()
- Does NOT use max() or min() (manual comparison only)
- Roll number is the unique dictionary key for students
- 8 manual edge cases handled
- Counts Eligible, Warning, Shortage
"""

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------
EXPENSE_CATEGORIES = ("Food", "Travel", "Utilities", "Stationery", "Other")
TAX_RATE = 0.18
PASS_MARK = 35
ATTENDANCE_ELIGIBLE = 75


# ---------------------------------------------------------------------------
# INPUT VALIDATION (ival)
# ---------------------------------------------------------------------------
def ival(value, vtype=float, min_val=None, max_val=None):
    """
    Input validation function (ival).
    Converts and validates a single value.
    Raises ValueError if conversion fails or constraints are violated.
    """
    try:
        converted = vtype(value)
    except (ValueError, TypeError):
        raise ValueError("Invalid input: could not convert value")

    if vtype == float and converted < 0:
        raise ValueError("Invalid input: value cannot be negative")

    if min_val is not None and converted < min_val:
        raise ValueError(f"Invalid input: value must be >= {min_val}")

    if max_val is not None and converted > max_val:
        raise ValueError(f"Invalid input: value must be <= {max_val}")

    return converted


# ---------------------------------------------------------------------------
# EXPENSE MANAGEMENT FUNCTIONS
# ---------------------------------------------------------------------------
def calculate_discount(subtotal):
    """Return discount rate based on subtotal slabs (no max/min used)."""
    if subtotal >= 10000:
        return 0.15
    elif subtotal >= 5000:
        return 0.10
    elif subtotal >= 1000:
        return 0.05
    else:
        return 0.0


def calculate_tax(taxable):
    """Calculate tax at TAX_RATE with .2f precision."""
    return round(taxable * TAX_RATE, 2)


# ---------------------------------------------------------------------------
# ATTENDANCE MANAGEMENT FUNCTIONS
# ---------------------------------------------------------------------------
def attendance_percentage(present, total_days):
    """Calculate attendance percentage. Raises ZeroDivisionError if total_days is 0."""
    if total_days == 0:
        raise ZeroDivisionError("Total days cannot be zero")
    return (present / total_days) * 100


def attendance_status(percentage):
    """Return Eligible / Warning / Shortage based on attendance percentage."""
    if percentage >= ATTENDANCE_ELIGIBLE:
        return "Eligible"
    elif percentage >= 60:
        return "Warning"
    else:
        return "Shortage"


def count_attendance_statuses(records):
    """
    Count number of students in each attendance category:
    Eligible, Warning, Shortage.
    Iterates using roll number (key) from the dictionary.
    """
    eligible = 0
    warning = 0
    shortage = 0
    for roll_no in records:
        status = records[roll_no]["status"]
        if status == "Eligible":
            eligible += 1
        elif status == "Warning":
            warning += 1
        elif status == "Shortage":
            shortage += 1
    return eligible, warning, shortage


# ---------------------------------------------------------------------------
# GRADING MANAGEMENT FUNCTIONS
# ---------------------------------------------------------------------------
def calculate_grade(percentage):
    """Return grade and remark based on percentage."""
    if percentage >= 90:
        return "A+", "Outstanding"
    elif percentage >= 80:
        return "A", "Excellent"
    elif percentage >= 70:
        return "B", "Very Good"
    elif percentage >= 60:
        return "C", "Good"
    elif percentage >= 50:
        return "D", "Satisfactory"
    elif percentage >= 35:
        return "E", "Pass"
    else:
        return "F", "Fail"


def count_grade_results(records):
    """
    Count Pass / Fail results using roll number as key.
    """
    pass_count = 0
    fail_count = 0
    for roll_no in records:
        if records[roll_no]["result"] == "PASS":
            pass_count += 1
        else:
            fail_count += 1
    return pass_count, fail_count


# ---------------------------------------------------------------------------
# MANUAL MAX / MIN (replacing built-in max() and min())
# ---------------------------------------------------------------------------
def manual_max(numbers):
    """Return the largest number in a list without using max()."""
    if not numbers:
        return None
    largest = numbers[0]
    for n in numbers[1:]:
        if n > largest:
            largest = n
    return largest


def manual_min(numbers):
    """Return the smallest number in a list without using min()."""
    if not numbers:
        return None
    smallest = numbers[0]
    for n in numbers[1:]:
        if n < smallest:
            smallest = n
    return smallest


# ---------------------------------------------------------------------------
# FORMATTING HELPERS (.2f)
# ---------------------------------------------------------------------------
def format_2f(value):
    """Format a numeric value to 2 decimal places."""
    return f"{value:.2f}"


def format_marks_list(marks):
    """Format a list of marks to 2 decimal places each using .2f."""
    return [f"{m:.2f}" for m in marks]


# ---------------------------------------------------------------------------
# ROLL NUMBER VALIDATION (unique key)
# ---------------------------------------------------------------------------
def validate_roll_no(roll_no):
    """Validate roll number: must not be empty."""
    if not roll_no or not roll_no.strip():
        raise ValueError("Edge Case 1: Roll No cannot be empty")
    return roll_no.strip()


def check_duplicate_roll(records, roll_no):
    """Check if roll number already exists (must be unique key)."""
    if roll_no in records:
        raise ValueError("Edge Case 2: Roll No already exists. Roll numbers must be unique.")
    return False


def student_exists(records, roll_no):
    """Check if a student with given roll number exists (Edge Case 8)."""
    return roll_no in records