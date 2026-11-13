"""
Expense | Attendance | Grading | Billing Management System (CLI)

Requirements met:
- CLI based (no GUI) - input() for all user input
- ival() function for input validation
- map() function for input processing
- .2f formatting used throughout
- No eval() used
- No max() or min() - manual comparison only
- Roll number is unique key in student dictionary
- Counts Eligible, Warning, and Shortage
- Grading scale linked to roll number
- 8 manual edge cases handled
"""

from datetime import date

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------
EXPENSE_CATEGORIES = ("Food", "Travel", "Utilities", "Stationery", "Other")
PASS_MARK = 35
ATTENDANCE_ELIGIBLE = 75
TAX_RATE = 0.18

# ---------------------------------------------------------------------------
# GLOBAL DATA STORES (dictionaries with roll number / id as unique key)
# ---------------------------------------------------------------------------
expenses = {}
attendance_records = {}
students = {}       # Key: roll number (unique)
bills = {}
expense_counter = 0
bill_counter = 0


# ---------------------------------------------------------------------------
# INPUT VALIDATION (ival)
# ---------------------------------------------------------------------------
def ival(value, vtype=float, min_val=None, max_val=None):
    """
    Input validation function.
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
# MANUAL MAX / MIN (replacing built-in max() and min())
# ---------------------------------------------------------------------------
def manual_max(items, key_func=None):
    """Return item with largest value without using max()."""
    if not items:
        return None
    best = items[0]
    best_val = key_func(best) if key_func else best
    for item in items[1:]:
        val = key_func(item) if key_func else item
        if val > best_val:
            best = item
            best_val = val
    return best


def manual_min(items, key_func=None):
    """Return item with smallest value without using min()."""
    if not items:
        return None
    best = items[0]
    best_val = key_func(best) if key_func else best
    for item in items[1:]:
        val = key_func(item) if key_func else item
        if val < best_val:
            best = item
            best_val = val
    return best


# ---------------------------------------------------------------------------
# FORMATTING HELPERS (.2f)
# ---------------------------------------------------------------------------
def format_2f(value):
    """Format a numeric value to 2 decimal places."""
    return f"{value:.2f}"


# ---------------------------------------------------------------------------
# ROLL NUMBER / ID VALIDATION (unique key)
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


def record_exists(records, roll_no):
    """Check if a record with given roll number exists (Edge Case 8)."""
    return roll_no in records


# ---------------------------------------------------------------------------
# EXPENSE MODULE
# ---------------------------------------------------------------------------
def add_expense():
    """Add an expense using ival()."""
    global expense_counter
    print("\n--- ADD EXPENSE ---")
    try:
        description = input("Description: ").strip()
        if not description:
            print("Edge Case: Description cannot be empty.")
            return

        print(f"Categories: {', '.join(EXPENSE_CATEGORIES)}")
        category = input("Category: ").strip().title()
        if category not in EXPENSE_CATEGORIES:
            print("Edge Case: Invalid category selected.")
            return

        amount_input = input("Amount: ").strip()
        amount = ival(amount_input, float, min_val=0.01)

        expense_counter += 1
        exp_id = f"E{expense_counter:04d}"
        expenses[exp_id] = {
            "description": description,
            "category": category,
            "amount": amount,
        }
        print(f"Expense saved: {description} | {category} | {format_2f(amount)}")

    except ValueError as e:
        print(f"Input Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def view_expenses():
    """View all expenses."""
    if not expenses:
        print("No expense records available.")
        return
    print("\n{:<10} {:<25} {:<15} {:>12}".format("EXP ID", "DESCRIPTION", "CATEGORY", "AMOUNT"))
    print("-" * 64)
    for exp_id, item in expenses.items():
        print("{:<10} {:<25} {:<15} {:>12.2f}".format(
            exp_id, item["description"][:24], item["category"], item["amount"]
        ))
    print("-" * 64)
    total = 0.0
    for item in expenses.values():
        total += item["amount"]
    print(f"{'TOTAL':<50}{total:>14.2f}")


def expense_summary():
    """Expense summary with manual max/min (no built-in max/min)."""
    if not expenses:
        print("No expense records available.")
        return
    totals = {category: 0.0 for category in EXPENSE_CATEGORIES}
    for item in expenses.values():
        totals[item["category"]] += item["amount"]

    print("\nEXPENSE SUMMARY")
    print("{:<18} {:>12}".format("CATEGORY", "TOTAL"))
    print("-" * 32)
    for category, total in totals.items():
        print("{:<18} {:>12.2f}".format(category, total))
    print("-" * 32)
    grand_total = sum(totals.values())
    print("{:<18} {:>12.2f}".format("GRAND TOTAL", grand_total))

    # Manual max/min on expense amounts
    amounts = list(totals.values())
    highest_cat = manual_max(list(totals.items()), key_func=lambda x: x[1])
    lowest_cat = manual_min(list(totals.items()), key_func=lambda x: x[1])
    print(f"Highest category: {highest_cat[0]} - {format_2f(highest_cat[1])}")
    print(f"Lowest category : {lowest_cat[0]} - {format_2f(lowest_cat[1])}")


def expense_menu():
    while True:
        print("\n--- EXPENSE MANAGEMENT ---")
        print("1. Add Expense\n2. View All Expenses\n3. Expense Summary\n4. Back")
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            expense_summary()
        elif choice == "4":
            break
        else:
            print("Invalid choice! Please enter 1-4.")


# ---------------------------------------------------------------------------
# ATTENDANCE MODULE
# ---------------------------------------------------------------------------
def attendance_percentage(present, total_days):
    """Calculate attendance percentage. Raises ZeroDivisionError if total_days is 0."""
    if total_days == 0:
        raise ZeroDivisionError("Total days cannot be zero")
    return (present / total_days) * 100


def attendance_status(percentage):
    """Return Eligible / Warning / Shortage based on percentage."""
    if percentage >= ATTENDANCE_ELIGIBLE:
        return "Eligible"
    elif percentage >= 60:
        return "Warning"
    else:
        return "Shortage"


def mark_attendance():
    """Mark attendance using roll number as unique key and map() for input."""
    print("\n--- MARK ATTENDANCE ---")
    try:
        roll_no = input("Enter Roll Number (unique): ").strip()
        validate_roll_no(roll_no)
        check_duplicate_roll(attendance_records, roll_no)

        name = input("Enter Student Name: ").strip()
        if not name:
            print("Edge Case: Name cannot be empty.")
            return

        total_days_input = input("Total working days: ").strip()
        total_days = ival(total_days_input, int, min_val=1)

        count_input = input("Number of people to enter: ").strip()
        count = ival(count_input, int, min_val=1)

        for _ in range(count):
            person_roll = input("Enter Roll Number (unique): ").strip()
            validate_roll_no(person_roll)
            check_duplicate_roll(attendance_records, person_roll)

            person_name = input("Enter Name: ").strip()
            if not person_name:
                print("Edge Case: Name cannot be empty. Skipping...")
                continue

            # map() used to process input: total_days and present days
            days_input = input("Enter Total Days and Present Days (space separated): ")
            total_d, present = map(int, days_input.split())
            total_d = ival(total_d, int, min_val=1)
            present = ival(present, int, min_val=0)

            percentage = attendance_percentage(present, total_d)
            status = attendance_status(percentage)

            attendance_records[person_roll] = {
                "name": person_name,
                "total_days": total_d,
                "present": present,
                "percentage": percentage,
                "status": status,
            }
            print(f"Attendance saved for {person_name} (Roll: {person_roll}) - {status} ({format_2f(percentage)}%)")

    except ValueError as e:
        print(f"Input Error: {e}")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def count_attendance_statuses(records):
    """Count Eligible, Warning, Shortage using roll number as key."""
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


def attendance_summary():
    """Attendance summary with counts and manual max/min."""
    if not attendance_records:
        print("No attendance records available.")
        return

    print("\n" + "=" * 70)
    print(f"{'ROLL NO':<12} {'NAME':<20} {'TOTAL':<8} {'PRESENT':<9} {'%':<8} {'STATUS':<12}")
    print("-" * 70)

    percentages = []
    for roll_no in attendance_records:
        rec = attendance_records[roll_no]
        print(f"{roll_no:<12} {rec['name']:<20} {rec['total_days']:<8} "
              f"{rec['present']:<9} {rec['percentage']:.2f}   {rec['status']:<12}")
        percentages.append(rec["percentage"])

    eligible_count, warning_count, shortage_count = count_attendance_statuses(attendance_records)

    print("-" * 70)
    print(f"Total Students: {len(attendance_records)}")
    print(f"Eligible: {eligible_count}  |  Warning: {warning_count}  |  Shortage: {shortage_count}")

    if percentages:
        avg_pct = sum(percentages) / len(percentages)
        highest_rec = manual_max(percentages)
        lowest_rec = manual_min(percentages)
        print(f"Average Attendance: {format_2f(avg_pct)}%")
        print(f"Highest Attendance: {format_2f(highest_rec)}%")
        print(f"Lowest Attendance: {format_2f(lowest_rec)}%")
    print("=" * 70)


def attendance_menu():
    while True:
        print("\n--- ATTENDANCE MANAGEMENT ---")
        print("1. Add Attendance Records\n2. View Attendance Summary\n3. Back")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            mark_attendance()
        elif choice == "2":
            attendance_summary()
        elif choice == "3":
            break
        else:
            print("Invalid choice! Please enter 1-3.")


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


def add_student_result():
    """Add student marks using roll number as unique key and map() for input."""
    print("\n--- STUDENT GRADING ---")
    try:
        roll_no = input("Enter Roll Number (unique): ").strip()
        validate_roll_no(roll_no)
        check_duplicate_roll(students, roll_no)

        name = input("Enter Student Name: ").strip()
        if not name:
            print("Edge Case: Name cannot be empty.")
            return

        subject_count_input = input("Number of subjects: ").strip()
        subject_count = ival(subject_count_input, int, min_val=1)

        # map() used to convert input marks to floats
        marks_input = input(f"Enter {subject_count} marks separated by space: ")
        marks = list(map(float, marks_input.split()))

        if len(marks) != subject_count:
            print(f"Edge Case: Expected {subject_count} marks, got {len(marks)}. Using available marks.")
            subject_count = len(marks)

        # Validate each mark using ival()
        validated_marks = []
        for m in marks:
            validated_marks.append(ival(m, float, min_val=0, max_val=100))

        total = 0.0
        for mark in validated_marks:
            total += mark

        average = total / subject_count if subject_count > 0 else 0.0
        percentage = average
        grade, remark = calculate_grade(percentage)

        result = "PASS"
        for mark in validated_marks:
            if mark < PASS_MARK:
                result = "FAIL"
                break

        students[roll_no] = {
            "name": name,
            "marks": validated_marks,
            "total": total,
            "average": average,
            "percentage": percentage,
            "grade": grade,
            "remark": remark,
            "result": result,
        }

        print(f"\nGrades saved for {name} (Roll: {roll_no})")
        print(f"Total: {format_2f(total)}  Average: {format_2f(average)}%  Grade: {grade}  Result: {result}")

    except ValueError as e:
        print(f"Input Error: {e}")
    except ZeroDivisionError:
        print("Cannot divide by zero. Enter at least one subject.")
    except Exception as e:
        print(f"Error: {e}")


def count_grade_results(records):
    """Count Pass/Fail using roll number as key."""
    pass_count = 0
    fail_count = 0
    for roll_no in records:
        if records[roll_no]["result"] == "PASS":
            pass_count += 1
        else:
            fail_count += 1
    return pass_count, fail_count


def class_summary():
    """Class summary using manual max/min (no built-in max/min)."""
    if not students:
        print("No student records available.")
        return

    print("\n" + "=" * 70)
    print(f"{'ROLL NO':<12} {'NAME':<20} {'TOTAL':<10} {'AVG %':<10} {'GRADE':<8} {'RESULT':<8}")
    print("-" * 70)

    percentages = []
    for roll_no in students:
        rec = students[roll_no]
        print(f"{roll_no:<12} {rec['name']:<20} {rec['total']:<10.2f} "
              f"{rec['average']:.2f}   {rec['grade']:<8} {rec['result']:<8}")
        percentages.append(rec["percentage"])

    pass_count, fail_count = count_grade_results(students)

    print("-" * 70)
    print(f"Total Students: {len(students)}")
    print(f"Pass: {pass_count}  |  Fail: {fail_count}")

    if percentages:
        avg_class = sum(percentages) / len(percentages)
        highest = manual_max(percentages)
        lowest = manual_min(percentages)
        print(f"Class Average: {format_2f(avg_class)}%")
        print(f"Highest Percentage: {format_2f(highest)}%")
        print(f"Lowest Percentage: {format_2f(lowest)}%")
    print("=" * 70)


def grading_menu():
    while True:
        print("\n--- GRADING SYSTEM ---")
        print("1. Add Student Marks\n2. Class Summary\n3. Back")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            add_student_result()
        elif choice == "2":
            class_summary()
        elif choice == "3":
            break
        else:
            print("Invalid choice! Please enter 1-3.")


# ---------------------------------------------------------------------------
# BILLING MODULE
# ---------------------------------------------------------------------------
def calculate_discount(subtotal):
    """Return discount rate based on subtotal slabs."""
    if subtotal >= 10000:
        return 0.15
    elif subtotal >= 5000:
        return 0.10
    elif subtotal >= 1000:
        return 0.05
    return 0.0


def calculate_tax(taxable_amount, tax_rate=TAX_RATE):
    """Calculate tax at TAX_RATE with .2f precision."""
    return round(taxable_amount * tax_rate, 2)


def generate_invoice():
    """Create customer bill."""
    global bill_counter
    print("\n--- CREATE CUSTOMER BILL ---")
    try:
        customer = input("Customer name: ").strip()
        if not customer:
            print("Edge Case: Customer name cannot be empty.")
            return

        bill_counter += 1
        bill_number = f"B-{bill_counter:04d}"

        items_input = input("Enter items (name:price:qty, comma separated): ").strip()
        if not items_input:
            print("Edge Case: No items entered.")
            return

        # map() used to process each item string
        item_parts = list(map(str.strip, items_input.split(",")))
        items = []
        for part in item_parts:
            try:
                name, price_str, qty_str = part.split(":")
                price = ival(price_str, float, min_val=0.01)
                qty = ival(qty_str, int, min_val=1)
                items.append({
                    "name": name.strip(),
                    "price": price,
                    "quantity": qty,
                    "total": round(price * qty, 2)
                })
            except ValueError:
                print(f"Skipping invalid item: {part}")
                continue

        if not items:
            print("No valid items added. Bill was not created.")
            return

        subtotal = 0.0
        for item in items:
            subtotal += item["total"]

        discount_rate = calculate_discount(subtotal)
        discount_amount = round(subtotal * discount_rate, 2)
        taxable = round(subtotal - discount_amount, 2)
        tax_amount = calculate_tax(taxable)
        grand_total = round(taxable + tax_amount, 2)

        bill = {
            "bill_number": bill_number,
            "date": date.today().isoformat(),
            "customer": customer,
            "items": items,
            "subtotal": subtotal,
            "discount_rate": discount_rate,
            "discount_amount": discount_amount,
            "taxable": taxable,
            "tax_amount": tax_amount,
            "grand_total": grand_total,
        }
        bills[bill_number] = bill
        print_invoice(bill)

    except ValueError as e:
        print(f"Input Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def print_invoice(bill):
    """Print formatted invoice with .2f."""
    print("\n" + "=" * 54)
    print("                     INVOICE")
    print("=" * 54)
    print(f"Bill No: {bill['bill_number']}    Date: {bill['date']}")
    print(f"Customer: {bill['customer']}")
    print("-" * 54)
    print("{:<22} {:>9} {:>5} {:>12}".format("ITEM", "PRICE", "QTY", "TOTAL"))
    for item in bill["items"]:
        print("{:<22} {:>9.2f} {:>5} {:>12.2f}".format(
            item["name"][:21], item["price"], item["quantity"], item["total"]
        ))
    print("-" * 54)
    print(f"{'Subtotal':<38}{bill['subtotal']:>16.2f}")
    print(f"{'Discount (' + str(int(bill['discount_rate'] * 100)) + '%)':<38}-{bill['discount_amount']:>15.2f}")
    print(f"{'Taxable amount':<38}{bill['taxable']:>16.2f}")
    print(f"{'Tax (18%)':<38}{bill['tax_amount']:>16.2f}")
    print("-" * 54)
    print(f"{'GRAND TOTAL':<38}{bill['grand_total']:>16.2f}")
    print("=" * 54)
    print("Thank you for your purchase!")


def billing_menu():
    while True:
        print("\n--- BILLING SYSTEM ---")
        print("1. Create Bill\n2. View Previous Bills\n3. Back")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            generate_invoice()
        elif choice == "2":
            if not bills:
                print("No bills available.")
            else:
                for bill_no in bills:
                    bill = bills[bill_no]
                    print(f"{bill['bill_number']} | {bill['customer']} | {format_2f(bill['grand_total'])}")
        elif choice == "3":
            break
        else:
            print("Invalid choice! Please enter 1-3.")


# ---------------------------------------------------------------------------
# REPORTS
# ---------------------------------------------------------------------------
def view_reports():
    while True:
        print("\n--- REPORTS ---")
        print("1. Expense Report\n2. Attendance Report\n3. Class Report")
        print("4. Billing Report\n5. Back")
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            view_expenses()
            expense_summary()
        elif choice == "2":
            attendance_summary()
        elif choice == "3":
            class_summary()
        elif choice == "4":
            if not bills:
                print("No billing records available.")
            else:
                for bill_no in bills:
                    bill = bills[bill_no]
                    print(f"{bill['bill_number']} | {bill['customer']} | {format_2f(bill['grand_total'])}")
        elif choice == "5":
            break
        else:
            print("Invalid choice! Please enter 1-5.")


# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------
def display_menu():
    print("\n" + "=" * 52)
    print(" EXPENSE | ATTENDANCE | GRADING | BILLING")
    print("=" * 52)
    print("1. Expense Management")
    print("2. Attendance Management")
    print("3. Grading System")
    print("4. Billing System")
    print("5. View Reports")
    print("6. Exit")
    print("-" * 52)


def main():
    while True:
        display_menu()
        try:
            choice = input("Enter your choice (1-6): ").strip()
        except EOFError:
            print("\nExiting... Goodbye!")
            break

        if choice == "1":
            expense_menu()
        elif choice == "2":
            attendance_menu()
        elif choice == "3":
            grading_menu()
        elif choice == "4":
            billing_menu()
        elif choice == "5":
            view_reports()
        elif choice == "6":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1-6.")


if __name__ == "__main__":
    main()