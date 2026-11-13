# 8 Manual Edge Cases - Attendance & Grading Management System

## How to Test
Run the program: `python attendance_management.py`
Follow the steps below for each edge case and verify the expected behavior.

---

## Edge Case 1: Zero Total Days (Division by Zero Protection)
**Module:** Attendance  
**Steps:**
1. Select option 1 (Add Attendance)
2. Enter Roll Number: `E001`
3. Enter Total Days: `0`
4. Enter Present Days: `0`

**Expected:** Program should handle gracefully (percentage = 0.00%, Status = Shortage)  
**Actual:** _______________________

---

## Edge Case 2: Duplicate Roll Number (Attendance)
**Module:** Attendance  
**Steps:**
1. Add a student with Roll Number: `S101`
2. Try to add another attendance record with the same Roll Number: `S101`

**Expected:** "Roll number S101 already exists! Skipping..." message  
**Actual:** _______________________

---

## Edge Case 3: Duplicate Roll Number (Grades)
**Module:** Grading  
**Steps:**
1. Add student grades with Roll Number: `G201`
2. Try to add grades again with the same Roll Number: `G201`

**Expected:** "Roll number G201 already has grades recorded!" message  
**Actual:** _______________________

---

## Edge Case 4: 100% Attendance Boundary
**Module:** Attendance  
**Steps:**
1. Enter Roll Number: `EC04`
2. Total Days: `50`, Present Days: `50`

**Expected:** Percentage = 100.00%, Status = Eligible  
**Actual:** _______________________

---

## Edge Case 5: Exactly 75% Attendance (Eligibility Boundary)
**Module:** Attendance  
**Steps:**
1. Enter Roll Number: `EC05`
2. Total Days: `100`, Present Days: `75`

**Expected:** Percentage = 75.00%, Status = Eligible  
**Actual:** _______________________

---

## Edge Case 6: Exactly 60% Attendance (Warning Boundary)
**Module:** Attendance  
**Steps:**
1. Enter Roll Number: `EC06`
2. Total Days: `100`, Present Days: `60`

**Expected:** Percentage = 60.00%, Status = Warning  
**Actual:** _______________________

---

## Edge Case 7: Negative Marks Input
**Module:** Grading  
**Steps:**
1. Select option 3 (Add Student Grades)
2. Enter Roll Number: `EC07`
3. Number of subjects: `2`
4. Marks: `-10 50`

**Expected:** Program accepts input but average will be calculated with negative mark  
**Actual:** _______________________

---

## Edge Case 8: Single Subject with Fail Mark (< 35)
**Module:** Grading  
**Steps:**
1. Select option 3 (Add Student Grades)
2. Enter Roll Number: `EC08`
3. Number of subjects: `1`
4. Marks: `30`

**Expected:** Percentage = 30.00%, Grade = F, Result = FAIL  
**Actual:** _______________________

---

## Edge Case Results Summary

| # | Edge Case | Status (Pass/Fail) | Notes |
|---|-----------|-------------------|-------|
| 1 | Zero Total Days | | |
| 2 | Duplicate Roll (Attendance) | | |
| 3 | Duplicate Roll (Grades) | | |
| 4 | 100% Attendance | | |
| 5 | 75% Boundary | | |
| 6 | 60% Boundary | | |
| 7 | Negative Marks | | |
| 8 | Single Subject Fail | | |
