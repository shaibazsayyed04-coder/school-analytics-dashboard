from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    standard = db.Column(db.Integer, nullable=False)
    roll_no = db.Column(db.Integer, nullable=False)
    parent_name = db.Column(db.String(100))
    parent_email = db.Column(db.String(100))


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.id"), nullable=False
    )
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)


class Fee(db.Model):
    __tablename__ = "fees"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.id"), nullable=False
    )
    total_fee = db.Column(db.Float)
    paid_amount = db.Column(db.Float)
    due_amount = db.Column(db.Float)


class Exam(db.Model):
    __tablename__ = "exams"

    id = db.Column(db.Integer, primary_key=True)
    standard = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(50))
    exam_date = db.Column(db.Date)
    exam_type = db.Column(db.String(20))
