from app import app
from models import db
from models import Student, Attendance, Fee
from datetime import date, timedelta
import random

with app.app_context():

    db.drop_all()
    db.create_all()

    students = []
    for std in range(1, 11):           
        for r in range(1, 51):         
            s = Student(
                name=f"Student_{std}_{r}",
                standard=std,
                roll_no=r,
                parent_name=f"Parent_{std}_{r}",
                parent_email=f"parent_{std}_{r}@example.com"
            )
            students.append(s)
            db.session.add(s)

    db.session.commit()
    print(f"✅ Created {len(students)} students")

    start_date = date(2025, 6, 1)
    days = 60

    for s in students:
        for i in range(days):
            d = start_date + timedelta(days=i)

            if d.weekday() >= 5:
                continue

            status = "Present" if random.random() > 0.25 else "Absent"
            att = Attendance(student_id=s.id, date=d, status=status)
            db.session.add(att)

    db.session.commit()
    print("✅ Attendance records created")

    for s in students:
        total_fee = 20000
        paid = random.choice([20000, 15000, 10000, 5000])
        fee = Fee(
            student_id=s.id,
            total_fee=total_fee,
            paid_amount=paid,
            due_amount=total_fee - paid,
        )
        db.session.add(fee)

    db.session.commit()
    print("✅ Fee records created")
    print("🎉 Seeding complete!")
