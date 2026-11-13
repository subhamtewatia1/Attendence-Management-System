from datetime import date

EXPENSE_CATEGORIES = ("Food", "Travel", "Utilities", "Stationery", "Other")
PASS_MARK = 35
ATTENDANCE_ELIGIBLE = 75
TAX_RATE = 0.18

expenses = []
attendance_records = []
students = []
bills = []


def get_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Enter a value of at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Enter a value no greater than {max_val}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Enter a value of at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Enter a value no greater than {max_val}.")
                continue
            return round(value, 2)
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_name(prompt):
    while True:
        value = input(prompt).strip()
        if 2 <= len(value) <= 40 and all(part.isalpha() for part in value.split()):
            return value
        print("Name must contain 2-40 letters and spaces only.")


def get_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def get_choice(prompt, options):
    while True:
        value = input(prompt).strip().title()
        if value in options:
            return value
        print("Choose from: " + ", ".join(options))


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


def add_expense():
    print("\n--- ADD EXPENSE ---")
    description = get_nonempty("Description: ")
    category = get_choice(
        "Category (Food/Travel/Utilities/Stationery/Other): ",
        EXPENSE_CATEGORIES
    )
    amount = get_float("Amount: ", 0.01)
    expenses.append({
        "description": description,
        "category": category,
        "amount": amount
    })
    print("Expense saved successfully!")


def view_expenses():
    if not expenses:
        print("No expense records available.")
        return
    print("\n{:<25} {:<15} {:>12}".format("DESCRIPTION", "CATEGORY", "AMOUNT"))
    print("-" * 54)
    for item in expenses:
        print("{:<25} {:<15} {:>12.2f}".format(
            item["description"][:24], item["category"], item["amount"]
        ))
    print("-" * 54)
    print(f"{'TOTAL':<40}{sum(x['amount'] for x in expenses):>14.2f}")


def expense_summary():
    if not expenses:
        print("No expense records available.")
        return
    totals = {category: 0.0 for category in EXPENSE_CATEGORIES}
    for item in expenses:
        totals[item["category"]] += item["amount"]
    print("\nEXPENSE SUMMARY")
    print("{:<18} {:>12}".format("CATEGORY", "TOTAL"))
    print("-" * 32)
    for category, total in totals.items():
        print("{:<18} {:>12.2f}".format(category, total))
    print("-" * 32)
    print("{:<18} {:>12.2f}".format("GRAND TOTAL", sum(totals.values())))
    highest = max(expenses, key=lambda x: x["amount"])
    lowest = min(expenses, key=lambda x: x["amount"])
    print(f"Highest expense: {highest['description']} - {highest['amount']:.2f}")
    print(f"Lowest expense : {lowest['description']} - {lowest['amount']:.2f}")


def expense_menu():
    while True:
        print("\n--- EXPENSE MANAGEMENT ---")
        print("1. Add Expense\n2. View All Expenses\n3. Expense Summary\n4. Back")
        choice = get_int("Enter your choice (1-4): ", 1, 4)
        if choice == 1:
            add_expense()
        elif choice == 2:
            view_expenses()
        elif choice == 3:
            expense_summary()
        else:
            break


def attendance_percentage(present, total_days):
    return (present / total_days) * 100


def attendance_status(percentage):
    if percentage >= 75:
        return "Eligible"
    elif percentage >= 60:
        return "Warning"
    return "Shortage"


def mark_attendance():
    print("\n--- MARK ATTENDANCE ---")
    total_days = get_int("Total working days: ", 1)
    count = get_int("Number of people to enter: ", 1)
    for _ in range(count):
        name = get_name("Name: ")
        person_id = get_nonempty("ID: ")
        present = get_int("Days present: ", 0, total_days)
        percentage = attendance_percentage(present, total_days)
        attendance_records.append({
            "name": name, "id": person_id, "total_days": total_days,
            "present": present, "percentage": percentage,
            "status": attendance_status(percentage)
        })
        print(f"Attendance saved for {name}.")


def attendance_summary():
    if not attendance_records:
        print("No attendance records available.")
        return
    percentages = [x["percentage"] for x in attendance_records]
    highest = max(attendance_records, key=lambda x: x["percentage"])
    lowest = min(attendance_records, key=lambda x: x["percentage"])
    counts = {"Eligible": 0, "Warning": 0, "Shortage": 0}
    for item in attendance_records:
        counts[item["status"]] += 1
    print("\nATTENDANCE REPORT")
    print("{:<18} {:<12} {:>8} {:>12} {:<12}".format(
        "NAME", "ID", "PRESENT", "ATTENDANCE", "STATUS"
    ))
    print("-" * 68)
    for item in attendance_records:
        print("{:<18} {:<12} {:>8} {:>11.2f}% {:<12}".format(
            item["name"][:17], item["id"][:11], item["present"],
            item["percentage"], item["status"]
        ))
    print("-" * 68)
    print(f"Total people: {len(attendance_records)}")
    print(f"Average attendance: {sum(percentages) / len(percentages):.2f}%")
    print(f"Highest: {highest['name']} ({highest['percentage']:.2f}%)")
    print(f"Lowest: {lowest['name']} ({lowest['percentage']:.2f}%)")
    print("Eligible: {Eligible} | Warning: {Warning} | Shortage: {Shortage}".format(**counts))


def attendance_menu():
    while True:
        print("\n--- ATTENDANCE MANAGEMENT ---")
        print("1. Add Attendance Records\n2. View Attendance Summary\n3. Back")
        choice = get_int("Enter your choice (1-3): ", 1, 3)
        if choice == 1:
            mark_attendance()
        elif choice == 2:
            attendance_summary()
        else:
            break


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
    elif percentage >= 35:
        return "E", "Pass"
    return "F", "Fail"


def add_student_result():
    print("\n--- STUDENT GRADING ---")
    name = get_name("Student name: ")
    subject_count = get_int("Number of subjects (default 5; enter 5 if unsure): ", 1)
    marks = []
    subjects = []
    for index in range(subject_count):
        subject = get_nonempty(f"Subject {index + 1} name: ")
        mark = get_float(f"Marks in {subject} (0-100): ", 0, 100)
        subjects.append(subject)
        marks.append(mark)
    total = sum(marks)
    average = total / subject_count
    grade, remark = calculate_grade(average)
    result = "FAIL" if any(mark < PASS_MARK for mark in marks) else "PASS"
    record = {
        "name": name, "subjects": subjects, "marks": marks,
        "total": total, "average": average, "percentage": average,
        "grade": grade, "remark": remark, "result": result
    }
    students.append(record)
    generate_report_card(record)


def generate_report_card(record):
    print("\n" + "=" * 39)
    print("              REPORT CARD")
    print("=" * 39)
    print(f"Student: {record['name']}")
    print("-" * 39)
    print("{:<22} {:>10}".format("SUBJECT", "MARKS"))
    for subject, mark in zip(record["subjects"], record["marks"]):
        print("{:<22} {:>10.2f}".format(subject[:21], mark))
    print("-" * 39)
    print(f"Total      : {record['total']:.2f} / {len(record['marks']) * 100}")
    print(f"Average    : {record['average']:.2f}")
    print(f"Percentage : {record['percentage']:.2f}%")
    print(f"Grade      : {record['grade']} ({record['remark']})")
    print(f"Result     : {record['result']}")
    print("=" * 39)


def class_summary():
    if not students:
        print("No student records available.")
        return
    topper = max(students, key=lambda x: x["percentage"])
    passed = sum(1 for x in students if x["result"] == "PASS")
    failed = len(students) - passed
    class_average = sum(x["percentage"] for x in students) / len(students)
    print("\nCLASS SUMMARY")
    print(f"Students: {len(students)}")
    print(f"Class average: {class_average:.2f}%")
    print(f"Topper: {topper['name']} ({topper['percentage']:.2f}%)")
    print(f"Pass count: {passed}")
    print(f"Fail count: {failed}")


def grading_menu():
    while True:
        print("\n--- GRADING SYSTEM ---")
        print("1. Add Student Marks\n2. Class Summary\n3. Back")
        choice = get_int("Enter your choice (1-3): ", 1, 3)
        if choice == 1:
            add_student_result()
        elif choice == 2:
            class_summary()
        else:
            break


def calculate_discount(subtotal):
    if subtotal >= 10000:
        return 0.15
    elif subtotal >= 5000:
        return 0.10
    elif subtotal >= 1000:
        return 0.05
    return 0.0


def calculate_tax(taxable_amount, tax_rate=TAX_RATE):
    return round(taxable_amount * tax_rate, 2)


def generate_invoice():
    print("\n--- CREATE CUSTOMER BILL ---")
    customer = get_name("Customer name: ")
    bill_number = f"B-{len(bills) + 1:04d}"
    items = []
    while True:
        item_name = input("Item name (type 'done' to finish): ").strip()
        if item_name.lower() == "done":
            break
        if not item_name:
            print("Item name cannot be empty.")
            continue
        price = get_float("Unit price: ", 0.01)
        quantity = get_int("Quantity: ", 1)
        items.append({
            "name": item_name, "price": price,
            "quantity": quantity, "total": round(price * quantity, 2)
        })
    if not items:
        print("No items added. Bill was not created.")
        return
    subtotal = sum(item["total"] for item in items)
    discount_rate = calculate_discount(subtotal)
    discount_amount = round(subtotal * discount_rate, 2)
    taxable = round(subtotal - discount_amount, 2)
    tax_amount = calculate_tax(taxable)
    grand_total = round(taxable + tax_amount, 2)
    bill = {
        "bill_number": bill_number, "date": date.today().isoformat(),
        "customer": customer, "items": items, "subtotal": subtotal,
        "discount_rate": discount_rate, "discount_amount": discount_amount,
        "taxable": taxable, "tax_amount": tax_amount,
        "grand_total": grand_total
    }
    bills.append(bill)
    print_invoice(bill)


def print_invoice(bill):
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
        choice = get_int("Enter your choice (1-3): ", 1, 3)
        if choice == 1:
            generate_invoice()
        elif choice == 2:
            if not bills:
                print("No bills available.")
            else:
                for bill in bills:
                    print(f"{bill['bill_number']} | {bill['customer']} | {bill['grand_total']:.2f}")
        else:
            break


def export_report(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Report exported to {filename}")
    except OSError as error:
        print(f"Could not export report: {error}")


def view_reports():
    while True:
        print("\n--- REPORTS ---")
        print("1. Expense Report\n2. Attendance Report\n3. Class Report")
        print("4. Billing Report\n5. Export Combined Report\n6. Back")
        choice = get_int("Enter your choice (1-6): ", 1, 6)
        if choice == 1:
            view_expenses()
            expense_summary()
        elif choice == 2:
            attendance_summary()
        elif choice == 3:
            class_summary()
        elif choice == 4:
            if not bills:
                print("No billing records available.")
            else:
                for bill in bills:
                    print(f"{bill['bill_number']} | {bill['customer']} | {bill['grand_total']:.2f}")
        elif choice == 5:
            lines = ["EXPENSE REPORT"]
            lines.extend(
                f"{x['description']} | {x['category']} | {x['amount']:.2f}"
                for x in expenses
            )
            lines.append("\nATTENDANCE REPORT")
            lines.extend(
                f"{x['name']} | {x['id']} | {x['percentage']:.2f}% | {x['status']}"
                for x in attendance_records
            )
            lines.append("\nGRADING REPORT")
            lines.extend(
                f"{x['name']} | {x['percentage']:.2f}% | {x['grade']} | {x['result']}"
                for x in students
            )
            lines.append("\nBILLING REPORT")
            lines.extend(
                f"{x['bill_number']} | {x['customer']} | {x['grand_total']:.2f}"
                for x in bills
            )
            export_report("management_report.txt", "\n".join(lines))
        else:
            break
