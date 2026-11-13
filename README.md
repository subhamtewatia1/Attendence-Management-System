# Expense, Attendance, Grading & Billing Management System

## Files
- `functions.py`: reusable validation, calculation, module, and report functions.
- `main.py`: imports the functions, displays the main menu, and runs the application.

## Requirements
- Python 3.8 or later
- Standard Python library only
- No external packages required

## Run
Keep both Python files in the same folder, open a terminal in that folder, and run:

```bash
python main.py
```

## Modules
1. Expense management with category totals and highest/lowest expense.
2. Attendance percentage and Eligible/Warning/Shortage status.
3. Student grading with grade scale and subject-level fail rule.
4. Billing with discount slabs and 18% tax.
5. Reports and combined text-file export.

Data is stored in memory while the program is running. It is cleared when the program exits, except exported report text.
