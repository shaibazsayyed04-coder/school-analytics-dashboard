from flask import Flask, render_template, abort, request, Response
from models import db, Student, Attendance, Fee, Exam
from sqlalchemy import func  
import csv

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/")
def index():

    total_students = Student.query.count()

    student_attendance_percents = []
    students = Student.query.all()

    for s in students:
        total_days = Attendance.query.filter_by(student_id=s.id).count()
        if total_days == 0:
            continue
        present_days = Attendance.query.filter_by(
            student_id=s.id, status="Present"
        ).count()
        percent = (present_days / total_days) * 100
        student_attendance_percents.append(percent)

    if student_attendance_percents:
        avg_attendance = round(
            sum(student_attendance_percents) / len(student_attendance_percents), 1
        )
        below_75 = sum(1 for p in student_attendance_percents if p < 75)
    else:
        avg_attendance = 0
        below_75 = 0

    total_pending_fee = db.session.query(func.sum(Fee.due_amount)).scalar() or 0
    total_pending_fee = int(total_pending_fee)

    attendance_by_standard = []
    for std in range(1, 11):
        std_students = Student.query.filter_by(standard=std).all()
        percents = []
        for s in std_students:
            total_days = Attendance.query.filter_by(student_id=s.id).count()
            if total_days == 0:
                continue
            present_days = Attendance.query.filter_by(
                student_id=s.id, status="Present"
            ).count()
            percents.append((present_days / total_days) * 100)

        if percents:
            attendance_by_standard.append(
                round(sum(percents) / len(percents), 1)
            )
        else:
            attendance_by_standard.append(0)

    return render_template(
        "dashboard.html",
        total_students=total_students,
        avg_attendance=avg_attendance,
        below_75=below_75,
        total_pending_fee=total_pending_fee,
        attendance_by_standard=attendance_by_standard,
    )


@app.route("/low-attendance")
def low_attendance():
    export = request.args.get("export", default="", type=str).lower()

    students = Student.query.all()
    low_students = []

    for s in students:
        total_days = Attendance.query.filter_by(student_id=s.id).count()
        if total_days == 0:
            continue

        present_days = Attendance.query.filter_by(
            student_id=s.id, status="Present"
        ).count()

        percent = round((present_days / total_days) * 100, 1)

        if percent < 75:  
            low_students.append({
                "id": s.id,
                "name": s.name,
                "standard": s.standard,
                "roll_no": s.roll_no,
                "percent": percent
            })

    low_students.sort(key=lambda x: (x["standard"], x["roll_no"]))

    if export == "csv":
        def generate():

            yield ",".join(["ID", "Name", "Standard", "Roll No", "Attendance %"]) + "\n"
            for s in low_students:
                row = [
                    s["id"],
                    s["name"].replace(",", " "),
                    s["standard"],
                    s["roll_no"],
                    s["percent"],
                ]
                yield ",".join(map(str, row)) + "\n"

        headers = {
            "Content-Disposition": 'attachment; filename="low_attendance_students.csv"',
            "Content-Type": "text/csv; charset=utf-8"
        }
        return Response(generate(), headers=headers)

    return render_template("low_attendance.html", students=low_students)


@app.route("/student/<int:student_id>")
def student_detail(student_id):
    student = Student.query.get(student_id)
    if not student:
        return abort(404)

    total_days = Attendance.query.filter_by(student_id=student.id).count()
    present_days = Attendance.query.filter_by(
        student_id=student.id, status="Present"
    ).count()
    absent_days = Attendance.query.filter_by(
        student_id=student.id, status="Absent"
    ).count()

    if total_days > 0:
        percent = round((present_days / total_days) * 100, 1)
    else:
        percent = 0

    fee = Fee.query.filter_by(student_id=student.id).first()

    return render_template(
        "student_detail.html",
        student=student,
        total_days=total_days,
        present_days=present_days,
        absent_days=absent_days,
        percent=percent,
        fee=fee,
    )


@app.route("/fees-pending")
def fees_pending():
    export = request.args.get("export", default="", type=str).lower()

    fee_rows = Fee.query.filter(Fee.due_amount > 0).all()
    pending = []

    for f in fee_rows:
        s = Student.query.get(f.student_id)
        if not s:
            continue

        pending.append({
            "id": s.id,
            "name": s.name,
            "standard": s.standard,
            "roll_no": s.roll_no,
            "total_fee": int(f.total_fee),
            "paid": int(f.paid_amount),
            "due": int(f.due_amount),
        })

    pending.sort(key=lambda x: x["due"], reverse=True)

    if export == "csv":
        def generate():

            yield ",".join(["ID", "Name", "Standard", "Roll No", "Total Fee", "Paid", "Due"]) + "\n"
            for s in pending:
                row = [
                    s["id"],
                    s["name"].replace(",", " "),
                    s["standard"],
                    s["roll_no"],
                    s["total_fee"],
                    s["paid"],
                    s["due"],
                ]
                yield ",".join(map(str, row)) + "\n"

        headers = {
            "Content-Disposition": 'attachment; filename="fees_pending_students.csv"',
            "Content-Type": "text/csv; charset=utf-8"
        }
        return Response(generate(), headers=headers)

    return render_template("fees_pending.html", students=pending)


@app.route("/students")
def students_list():

    standard_filter = request.args.get("standard", type=int)
    search_q = request.args.get("q", default="", type=str).strip()
    export = request.args.get("export", default="", type=str).lower()  

    query = Student.query

    if standard_filter:
        query = query.filter_by(standard=standard_filter)

    if search_q:

        query = query.filter(Student.name.ilike(f"%{search_q}%"))

    students = query.order_by(Student.standard, Student.roll_no).all()

    if export == "csv":
        def generate():

            yield ",".join(["ID", "Name", "Standard", "Roll No", "Parent", "Email"]) + "\n"
            for s in students:
                row = [
                    s.id,
                    (s.name or "").replace(",", " "),
                    s.standard,
                    s.roll_no,
                    (s.parent_name or "").replace(",", " "),
                    (s.parent_email or "").replace(",", " "),
                ]
                yield ",".join(map(str, row)) + "\n"

        filename = "students_export.csv"
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": "text/csv; charset=utf-8"
        }
        return Response(generate(), headers=headers)

    return render_template(
        "students.html",
        students=students,
        selected_standard=standard_filter,
        search_q=search_q,
    )


if __name__ == "__main__":
    app.run(debug=True)
