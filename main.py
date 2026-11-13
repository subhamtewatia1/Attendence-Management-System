1
    display_menu,
    get_int,
    expense_menu,
    attendance_menu,
    grading_menu,
    billing_menu,
    view_reports
)


def main():
    try:
        while True:
            display_menu()
            choice = get_int("Enter your choice (1-6): ", 1, 6)

            if choice == 1:
                expense_menu()
            elif choice == 2:
                attendance_menu()
            elif choice == 3:
                grading_menu()
            elif choice == 4:
                billing_menu()
            elif choice == 5:
                view_reports()
            elif choice == 6:
                print("Thank you for using the system. Goodbye!")
                break

    except KeyboardInterrupt:
        print("\nProgram stopped safely. Goodbye!")


if __name__ == "__main__":
    main()
