# School Analytics Dashboard

A Flask-based web application to monitor **school attendance and fees** for 500+ students (Standards 1 to 10).  
Built as a practice project to learn **data analytics + full stack** concepts.

---

## 🎯 Project Overview

This project simulates a real school admin dashboard where the administrator can:

- Track **attendance** of students across classes 1–10
- Monitor **fee payments** and pending amounts
- Drill down to see **student-wise details**
- Export data to **CSV** for further analysis (Excel, Python, Power BI, etc.)

It is designed as a **data analytics + web development** portfolio project.

---

## ✨ Features

### 👨‍🎓 Student Management

- 500+ simulated students (Standards 1–10, ~50 students per class)
- **All Students** page:
  - Filter by **standard**
  - Search by **student name**
  - Click on a name to view detailed **student profile**

### 📊 Attendance Analytics

- Total number of students on the dashboard
- Overall **average attendance %**
- Count of **students below 75% attendance**
- Class-wise average attendance chart (Std 1–10) using **Chart.js**
- **Low Attendance** page:
  - Shows only students with attendance `< 75%`
  - Sorted by standard and roll number
  - Each name clickable → opens student detail page

### 💰 Fees Analytics

- Total **pending fee amount** on the main dashboard
- **Fees Pending** page:
  - Lists all students with due amounts
  - Shows total fee, paid amount, and pending amount
  - Sorted by highest due first
  - Names clickable → student detail view

### 📈 CSV Export

To support reporting and external analysis:

- Export **All Students** list → `students_export.csv`
- Export **Low Attendance** students → `low_attendance_students.csv`
- Export **Fees Pending** students → `fees_pending_students.csv`

CSV files can be opened in Excel / Google Sheets / Python / Power BI for further analytics.

---

## 👤 Student Detail Page

Each student has a dedicated detail page showing:

- Basic info: **name, standard, roll no, parent name, parent email**
- Attendance summary:
  - Total days
  - Present days
  - Absent days
  - Attendance %
  - Status badge:  
    - 🔴 “Below 75% – At Risk”  
    - 🟢 “Good Attendance”
- Fee summary:
  - Total fee, amount paid, and due amount
  - Badge for **Payment Pending** or **No Dues**

This screen can be treated as a **parent report view**.

---

## 🧱 Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite, SQLAlchemy
- **Frontend:** HTML, Bootstrap 5
- **Charts:** Chart.js
- **Others:** CSV export (custom generator functions)

---

## 📂 Project Structure (simplified)

```text
school-analytics/
│
├── app.py                # Main Flask application
├── models.py             # SQLAlchemy models (Student, Attendance, Fee, Exam)
├── data_seed.py          # Script to generate dummy data
│
├── templates/
│   ├── base.html         # Base layout + navbar
│   ├── dashboard.html    # Main dashboard view
│   ├── low_attendance.html
│   ├── fees_pending.html
│   ├── students.html     # All students list + search + filter
│   └── student_detail.html
│
└── static/
    ├── css/              # Custom styles
    └── js/               # Custom JS (Chart.js config)
