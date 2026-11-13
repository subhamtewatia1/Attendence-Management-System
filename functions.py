
from datetime import date

EXPENSE_CATEGORIES = ("Food", "Travel", "Utilities", "Stationery", "Other")
PASS_MARK = 35
ATTENDANCE_ELIGIBLE = 75
TAX_RATE = 0.18

expenses = {}
attendance_records = {}
students = {}
bills = {}

expense_counter = 0
bill_counter = 0


# INPUT VALIDATION

def eval(value, vtype=float, min_val=None, max_val=None):
    try:
        converted = vtype(value)

        if min_val is not None and converted < min_val:
            raise ValueError("Value is below the allowed limit.")

        if max_val is not None and converted > max_val:
            raise ValueError("Value is above the allowed limit.")

        return converted

    except (ValueError, TypeError):
        raise ValueError("Please enter a valid value.")


def format_2f(value):
    return f"{value:.2f}"


def validate_roll_no(roll_no):
    if not roll_no.strip():
        raise ValueError("Roll number cannot be empty.")

    return roll_no.strip()


def check_duplicate_roll(records, roll_no):
    if roll_no in records:
        raise ValueError("Roll number already exists.")


# MANUAL MAXIMUM AND MINIMUM

def manual_max(items, key_func=None):
    if not items:
        return None

    highest = items[0]

    for item in items:
        value = key_func(item) if key_func else item
        highest_value = key_func(highest) if key_func else highest

        if value > highest_value:
            highest = item

    return highest


def manual_min(items, key_func=None):
    if not items:
        return None

    lowest = items[0]

    for item in items:
        value = key_func(item) if key_func else item
        lowest_value = key_func(lowest) if key_func else lowest

        if value < lowest_value:
            lowest = item

    return lowest


# EXPENSE MODULE

def add_expense():
    global expense_counter

    print("\n--- ADD EXPENSE ---")

    try:
        description = input("Description: ").strip()

        if not description:
            raise ValueError("Description cannot be empty.")

        print("Categories:", ", ".join(EXPENSE_CATEGORIES))
        category = input("Category: ").strip().title()

        if category not in EXPENSE_CATEGORIES:
            raise ValueError("Invalid category.")

        amount = ival(input("Amount: "), float, min_val=0.01)

        expense_counter += 1
        exp_id = f"E{expense_counter:04d}"

        expenses[exp_id] = {
            "description": description,
            "category": category,
            "amount": amount
        }

        print("Expense added successfully.")

    except ValueError as e:
        print("Error:", e)


def view_expenses():
    if not expenses:
        print("No expenses available.")
        return

    print("\nEXPENSE RECORDS")
    print("-" * 65)

    total = 0.0

    for exp_id, item in expenses.items():
        print(
            f"{exp_id:<10} {item['description']:<20} "
            f"{item['category']:<15} {item['amount']:.2f}"
        )

        total += item["amount"]

    print("-" * 65)
    print(f"Total Expense: {total:.2f}")


def expense_summary():
    if not expenses:
        print("No expense records available.")
        return

    totals = {}

    for category in EXPENSE_CATEGORIES:
        totals[category] = 0.0

    for item in expenses.values():
        totals[item["category"]] += item["amount"]

    print("\nEXPENSE SUMMARY")

    for category, total in totals.items():
        print(f"{category:<15} {total:.2f}")

    grand_total = 0.0

    for total in totals.values():
        grand_total += total

    print(f"Grand Total: {grand_total:.2f}")

    highest = manual_max(list(totals.items()), key_func=lambda x: x[1])
    lowest = manual_min(list(totals.items()), key_func=lambda x: x[1])

    print(f"Highest Category: {highest[0]} - {highest[1]:.2f}")
    print(f"Lowest Category: {lowest[0]} - {lowest[1]:.2f}")


def expense_menu():
    while True:
        print("\n--- EXPENSE MANAGEMENT ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Expense Summary")
        print("4. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            expense_summary()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


# ATTENDANCE MODULE

def attendance_percentage(present, total_days):
    if total_days <= 0:
        raise ValueError("Total days must be greater than zero.")

    if present > total_days:
        raise ValueError("Present days cannot exceed total days.")

    return (present / total_days) * 100


def attendance_status(percentage):
    if percentage >= ATTENDANCE_ELIGIBLE:
        return "Eligible"
    elif percentage >= 60:
        return "Warning"
    else:
        return "Shortage"


def mark_attendance():
    print("\n--- MARK ATTENDANCE ---")

    try:
        count = ival(input("Number of students: "), int, min_val=1)

        for i in range(count):
            print(f"\nStudent {i + 1}")

            roll_no = validate_roll_no(input("Roll Number: "))
            check_duplicate_roll(attendance_records, roll_no)

            name = input("Student Name: ").strip()

            if not name:
                raise ValueError("Name cannot be empty.")

            days_input = input(
                "Enter total working days and present days: "
            )

            total_days, present = map(int, days_input.split())

            total_days = ival(total_days, int, min_val=1)
            present = ival(present, int, min_val=0)

            percentage = attendance_percentage(present, total_days)
            status = attendance_status(percentage)

            attendance_records[roll_no] = {
                "name": name,
                "total_days": total_days,
                "present": present,
                "percentage": percentage,
                "status": status
            }

            print(f"Attendance saved: {format_2f(percentage)}%")
            print("Status:", status)

    except ValueError as e:
        print("Error:", e)


def count_attendance_statuses():
    eligible = 0
    warning = 0
    shortage = 0

    for record in attendance_records.values():
        if record["status"] == "Eligible":
            eligible += 1
        elif record["status"] == "Warning":
            warning += 1
        else:
            shortage += 1

    return eligible, warning, shortage


def attendance_summary():
    if not attendance_records:
        print("No attendance records available.")
        return

    percentages = []

    print("\nATTENDANCE REPORT")
    print("-" * 75)

    for roll_no, record in attendance_records.items():
        print(
            f"{roll_no:<12} {record['name']:<18} "
            f"{record['present']:<8} "
            f"{record['percentage']:.2f}% "
            f"{record['status']}"
        )

        percentages.append(record["percentage"])

    eligible, warning, shortage = count_attendance_statuses()

    average = sum(percentages) / len(percentages)
    highest = manual_max(percentages)
    lowest = manual_min(percentages)

    print("-" * 75)
    print(f"Total Students: {len(attendance_records)}")
    print(f"Eligible: {eligible}")
    print(f"Warning: {warning}")
    print(f"Shortage: {shortage}")
    print(f"Average Attendance: {average:.2f}%")
    print(f"Highest Attendance: {highest:.2f}%")
    print(f"Lowest Attendance: {lowest:.2f}%")


def attendance_menu():
    while True:
        print("\n--- ATTENDANCE MANAGEMENT ---")
        print("1. Mark Attendance")
        print("2. Attendance Summary")
        print("3. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            mark_attendance()
        elif choice == "2":
            attendance_summary()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


# GRADING MODULE

def calculate_grade(percentage):
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
    elif percentage >= PASS_MARK:
        return "E", "Pass"
    else:
        return "F", "Fail"


def add_student_result():
    print("\n--- ADD STUDENT RESULT ---")

    try:
        roll_no = validate_roll_no(input("Roll Number: "))
        check_duplicate_roll(students, roll_no)

        name = input("Student Name: ").strip()

        if not name:
            raise ValueError("Name cannot be empty.")

        subject_count = ival(
            input("Number of subjects: "),
            int,
            min_val=1
        )

        marks_input = input("Enter marks separated by spaces: ")
        marks = list(map(float, marks_input.split()))

        if len(marks) != subject_count:
            raise ValueError("Number of marks does not match subjects.")

        validated_marks = []

        for mark in marks:
            validated_marks.append(
                ival(mark, float, min_val=0, max_val=100)
            )

        total = 0.0

        for mark in validated_marks:
            total += mark

        average = total / subject_count
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
            "result": result
        }

        print("\nResult saved successfully.")
        print(f"Total: {total:.2f}")
        print(f"Average: {average:.2f}")
        print(f"Grade: {grade}")
        print(f"Remark: {remark}")
        print(f"Result: {result}")

    except ValueError as e:
        print("Error:", e)


def count_grade_results():
    pass_count = 0
    fail_count = 0

    for record in students.values():
        if record["result"] == "PASS":
            pass_count += 1
        else:
            fail_count += 1

    return pass_count, fail_count


def class_summary():
    if not students:
        print("No student records available.")
        return

    percentages = []

    print("\nCLASS RESULT SUMMARY")
    print("-" * 75)

    for roll_no, record in students.items():
        print(
            f"{roll_no:<12} {record['name']:<18} "
            f"{record['total']:.2f} "
            f"{record['average']:.2f}% "
            f"{record['grade']:<6} {record['result']}"
        )

        percentages.append(record["percentage"])

    pass_count, fail_count = count_grade_results()

    average = sum(percentages) / len(percentages)
    highest = manual_max(percentages)
    lowest = manual_min(percentages)

    print("-" * 75)
    print(f"Total Students: {len(students)}")
    print(f"Pass: {pass_count} | Fail: {fail_count}")
    print(f"Class Average: {average:.2f}%")
    print(f"Highest Percentage: {highest:.2f}%")
    print(f"Lowest Percentage: {lowest:.2f}%")


def grading_menu():
    while True:
        print("\n--- GRADING SYSTEM ---")
        print("1. Add Student Marks")
        print("2. Class Summary")
        print("3. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_student_result()
        elif choice == "2":
            class_summary()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


# BILLING MODULE

def calculate_discount(subtotal):
    if subtotal >= 10000:
        return 0.15
    elif subtotal >= 5000:
        return 0.10
    elif subtotal >= 1000:
        return 0.05

    return 0.0


def calculate_tax(amount):
    return round(amount * TAX_RATE, 2)


def generate_invoice():
    global bill_counter

    print("\n--- CREATE BILL ---")

    try:
        customer = input("Customer Name: ").strip()

        if not customer:
            raise ValueError("Customer name cannot be empty.")

        items_input = input(
            "Enter items (name:price:quantity), separated by commas: "
        ).strip()

        if not items_input:
            raise ValueError("No items entered.")

        item_parts = list(map(str.strip, items_input.split(",")))
        items = []

        for part in item_parts:
            name, price_str, qty_str = part.split(":")

            if not name.strip():
                raise ValueError("Item name cannot be empty.")

            price = ival(price_str, float, min_val=0.01)
            quantity = ival(qty_str, int, min_val=1)

            items.append({
                "name": name.strip(),
                "price": price,
                "quantity": quantity,
                "total": round(price * quantity, 2)
            })

        subtotal = 0.0

        for item in items:
            subtotal += item["total"]

        discount_rate = calculate_discount(subtotal)
        discount = round(subtotal * discount_rate, 2)
        taxable = round(subtotal - discount, 2)
        tax = calculate_tax(taxable)
        grand_total = round(taxable + tax, 2)

        bill_counter += 1
        bill_number = f"B-{bill_counter:04d}"

        bill = {
            "bill_number": bill_number,
            "date": date.today().isoformat(),
            "customer": customer,
            "items": items,
            "subtotal": subtotal,
            "discount": discount,
            "tax": tax,
            "grand_total": grand_total
        }

        bills[bill_number] = bill

        print_invoice(bill)

    except ValueError as e:
        print("Error:", e)


def print_invoice(bill):
    print("\n" + "=" * 50)
    print("                  CUSTOMER INVOICE")
    print("=" * 50)

    print("Bill Number:", bill["bill_number"])
    print("Date:", bill["date"])
    print("Customer:", bill["customer"])

    print("-" * 50)

    for item in bill["items"]:
        print(
            f"{item['name']:<18} "
            f"{item['price']:>8.2f} "
            f"{item['quantity']:>5} "
            f"{item['total']:>10.2f}"
        )

    print("-" * 50)
    print(f"{'Subtotal':<35}{bill['subtotal']:>12.2f}")
    print(f"{'Discount':<35}{bill['discount']:>12.2f}")
    print(f"{'Tax (18%)':<35}{bill['tax']:>12.2f}")
    print("-" * 50)
    print(f"{'Grand Total':<35}{bill['grand_total']:>12.2f}")
    print("=" * 50)


def billing_menu():
    while True:
        print("\n--- BILLING SYSTEM ---")
        print("1. Create Bill")
        print("2. View Previous Bills")
        print("3. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            generate_invoice()

        elif choice == "2":
            if not bills:
                print("No bills available.")
            else:
                for bill in bills.values():
                    print(
                        f"{bill['bill_number']} | "
                        f"{bill['customer']} | "
                        f"{bill['grand_total']:.2f}"
                    )

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


# REPORTS MODULE

def view_reports():
    while True:
        print("\n--- REPORTS ---")
        print("1. Expense Report")
        print("2. Attendance Report")
        print("3. Class Report")
        print("4. Billing Report")
        print("5. Back")

        choice = input("Enter choice: ").strip()

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
                for bill in bills.values():
                    print(
                        f"{bill['bill_number']} | "
                        f"{bill['customer']} | "
                        f"{bill['grand_total']:.2f}"
                    )

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


# MAIN MENU

def main():
    while True:
        print("\n" + "=" * 50)
        print(" EXPENSE | ATTENDANCE | GRADING | BILLING")
        print("=" * 50)
        print("1. Expense Management")
        print("2. Attendance Management")
        print("3. Grading System")
        print("4. Billing System")
        print("5. View Reports")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

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
            print("Thank you for using the system.")
            break

        else:
            print("Invalid choice. Enter 1-6.")


if __name__ == "__main__":
    main()
