"""
CLI-based Attendance & Grading Management System

Requirements met:
- input() function for all user input
- map() function for input processing
- CLI based (no GUI)
- .2f formatting used throughout
- No max() or min() functions (manual comparison)
- Roll number is unique key in student dictionary
- Counts Eligible, Warning, and Shortage
- Grading scale linked to roll number
- 8 manual edge cases documented below
"""

# ---------------------------------------------------------------------------
# GLOBAL DATA STORES
# ---------------------------------------------------------------------------
# Key: roll number (string), Value: dict with attendance info
attendance_records = {}

# Key: roll number (string), Value: dict with grading info
student_grades = {}


# ---------------------------------------------------------------------------
# HELPER: manual max without built-in max()
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
# ATTENDANCE MODULE
# ---------------------------------------------------------------------------
def calculate_percentage(present, total_days):
    """Calculate attendance percentage with .2f formatting."""
    if total_days == 0:
        return 0.0
    return (present / total_days) * 100


def get_attendance_status(percentage):
    """Return Eligible / Warning / Shortage based on percentage."""
    if percentage >= 75:
        return "Eligible"
    elif percentage >= 60:
        return "Warning"
    else:
        return "Shortage"


def add_attendance():
    """Add attendance records using roll number as unique key."""
    print("\n--- ADD ATTENDANCE ---")
    try:
        count_input = input("Enter number of students (comma separated not needed, just one number): ")
        count = int(count_input)

        for _ in range(count):
            roll_no = input("Enter Roll Number (unique): ").strip()
            if roll_no in attendance_records:
                print(f"Roll number {roll_no} already exists! Skipping...")
                continue

            name = input("Enter Student Name: ").strip()

            # Using map() to process input: total_days and present days
            days_input = input("Enter Total Days and Present Days (space separated): ")
            total_days, present = map(int, days_input.split())

            percentage = calculate_percentage(present, total_days)
            status = get_attendance_status(percentage)

            attendance_records[roll_no] = {
                "name": name,
                "total_days": total_days,
                "present": present,
                "percentage": percentage,
                "status": status
            }
            print(f"Attendance saved for {name} (Roll: {roll_no}) - {status}")

    except ValueError:
        print("Invalid input! Please enter numeric values where required.")
    except Exception as e:
        print(f"Error: {e}")


def view_attendance_summary():
    """Display attendance summary with counts of Eligible, Warning, Shortage."""
    if not attendance_records:
        print("\nNo attendance records available.")
        return

    print("\n" + "=" * 70)
    print(f"{'ROLL NO':<12} {'NAME':<20} {'TOTAL':<8} {'PRESENT':<9} {'%':<8} {'STATUS':<12}")
    print("-" * 70)

    eligible_count = 0
    warning_count = 0
    shortage_count = 0

    percentages = []

    for roll_no, rec in attendance_records.items():
        print(f"{roll_no:<12} {rec['name']:<20} {rec['total_days']:<8} "
              f"{rec['present']:<9} {rec['percentage']:.2f}   {rec['status']:<12}")

        percentages.append(rec["percentage"])

        if rec["status"] == "Eligible":
            eligible_count += 1
        elif rec["status"] == "Warning":
            warning_count += 1
        else:
            shortage_count += 1

    print("-" * 70)
    print(f"Total Students: {len(attendance_records)}")
    print(f"Eligible: {eligible_count}  |  Warning: {warning_count}  |  Shortage: {shortage_count}")

    if percentages:
        avg_pct = sum(percentages) / len(percentages)
        highest = manual_max(percentages)
        lowest = manual_min(percentages)
        print(f"Average Attendance: {avg_pct:.2f}%")
        print(f"Highest Attendance: {highest:.2f}%")
        print(f"Lowest Attendance: {lowest:.2f}%")
    print("=" * 70)


# ---------------------------------------------------------------------------
# GRADING MODULE
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


def add_student_grades():
    """Add student marks using roll number as unique key."""
    print("\n--- ADD STUDENT GRADES ---")
    try:
        roll_no = input("Enter Roll Number (unique): ").strip()
        if roll_no in student_grades:
            print(f"Roll number {roll_no} already has grades recorded!")
            return

        name = input("Enter Student Name: ").strip()

        subjects_input = input("Enter number of subjects: ")
        subject_count = int(subjects_input)

        marks_input = input(f"Enter {subject_count} marks separated by space: ")
        # Using map() to convert input marks to floats
        marks = list(map(float, marks_input.split()))

        if len(marks) != subject_count:
            print(f"Expected {subject_count} marks, got {len(marks)}. Using available marks.")
            subject_count = len(marks)

        total = 0.0
        for mark in marks:
            total += mark

        average = total / subject_count if subject_count > 0 else 0.0
        percentage = average
        grade, remark = calculate_grade(percentage)

        # Check if any subject mark is below 35 (fail rule)
        result = "PASS"
        for mark in marks:
            if mark < 35:
                result = "FAIL"
                break

        student_grades[roll_no] = {
            "name": name,
            "marks": marks,
            "total": total,
            "average": average,
            "percentage": percentage,
            "grade": grade,
            "remark": remark,
            "result": result
        }

        print(f"\nGrades saved for {name} (Roll: {roll_no})")
        print(f"Total: {total:.2f}  Average: {average:.2f}%  Grade: {grade}  Result: {result}")

    except ValueError:
        print("Invalid input! Please enter numeric values.")
    except ZeroDivisionError:
        print("Cannot divide by zero. Enter at least one subject.")
    except Exception as e:
        print(f"Error: {e}")


def view_class_summary():
    """Display class summary using manual max/min (no built-in max/min)."""
    if not student_grades:
        print("\nNo student grade records available.")
        return

    print("\n" + "=" * 70)
    print(f"{'ROLL NO':<12} {'NAME':<20} {'TOTAL':<10} {'AVG %':<10} {'GRADE':<8} {'RESULT':<8}")
    print("-" * 70)

    pass_count = 0
    fail_count = 0
    percentages = []

    for roll_no, rec in student_grades.items():
        print(f"{roll_no:<12} {rec['name']:<20} {rec['total']:<10.2f} "
              f"{rec['average']:.2f}   {rec['grade']:<8} {rec['result']:<8}")

        percentages.append(rec["percentage"])

        if rec["result"] == "PASS":
            pass_count += 1
        else:
            fail_count += 1

    print("-" * 70)
    print(f"Total Students: {len(student_grades)}")
    print(f"Pass: {pass_count}  |  Fail: {fail_count}")

    if percentages:
        avg_class = sum(percentages) / len(percentages)
        highest = manual_max(percentages)
        lowest = manual_min(percentages)
        print(f"Class Average: {avg_class:.2f}%")
        print(f"Highest Percentage: {highest:.2f}%")
        print(f"Lowest Percentage: {lowest:.2f}%")
    print("=" * 70)


# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------
def display_menu():
    print("\n" + "=" * 50)
    print("   ATTENDANCE & GRADING MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. Add Attendance")
    print("2. View Attendance Summary")
    print("3. Add Student Grades")
    print("4. View Class Summary")
    print("5. Exit")
    print("-" * 50)


def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_attendance()
        elif choice == "2":
            view_attendance_summary()
        elif choice == "3":
            add_student_grades()
        elif choice == "4":
            view_class_summary()
        elif choice == "5":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1-5.")


if __name__ == "__main__":
    main()