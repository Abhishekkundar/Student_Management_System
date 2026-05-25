from flask import Flask, jsonify, render_template, request
import sqlite3 as sql


app = Flask(__name__, template_folder="Templates", static_folder="Static")
DB_NAME = "student.db"


def get_db_connection():
    conn = sql.connect(DB_NAME)
    conn.row_factory = sql.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            total_subjects INTEGER NOT NULL,
            total_marks INTEGER NOT NULL,
            percentage REAL NOT NULL,
            grade TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            marks INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        )
        """
    )

    conn.commit()
    conn.close()


def grade_check(percent):
    if percent >= 80:
        return "Distinction"
    if percent >= 70:
        return "First Class"
    if percent >= 60:
        return "Second Class"
    if percent > 35:
        return "Pass"
    return "Fail"


def format_student(row, subjects):
    return {
        "name": row["name"],
        "department": row["department"],
        "subjects_list": subjects,
        "no_sub": row["total_subjects"],
        "Total_marks": row["total_marks"],
        "Percentage": row["percentage"],
        "Grade": row["grade"],
    }


@app.route("/",methods=["GET"])
def login():
    return render_template("login.html")
@app.route("/dashboard")
def index():
    return render_template("index.html")


@app.route("/api/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    student_rows = conn.execute("SELECT * FROM students ORDER BY id").fetchall()

    students = {}
    for student in student_rows:
        subject_rows = conn.execute(
            "SELECT subject, marks FROM subjects WHERE student_id = ? ORDER BY id",
            (student["id"],),
        ).fetchall()
        subjects = [
            {"subject": subject["subject"], "marks": subject["marks"]}
            for subject in subject_rows
        ]
        students[student["id"]] = format_student(student, subjects)

    conn.close()
    return jsonify(students)


@app.route("/api/add", methods=["POST"])
def add_student():
    data = request.get_json() or {}

    st_id = str(data.get("id", "")).strip()
    name = str(data.get("name", "")).strip()
    department = str(data.get("department", "")).strip()
    subjects_list = data.get("subjects_list") or []

    if not st_id or not name or not department:
        return jsonify({"error": "Student ID, name, and department are required"}), 400

    if not subjects_list:
        return jsonify({"error": "Add at least one subject"}), 400

    cleaned_subjects = []
    for item in subjects_list:
        subject = str(item.get("subject", "")).strip()
        try:
            marks = int(item.get("marks"))
        except (TypeError, ValueError):
            return jsonify({"error": "Marks must be a number"}), 400

        if not subject:
            return jsonify({"error": "Subject name cannot be empty"}), 400
        if marks < 0 or marks > 100:
            return jsonify({"error": "Marks must be between 0 and 100"}), 400

        cleaned_subjects.append({"subject": subject, "marks": marks})

    total_subjects = len(cleaned_subjects)
    total_marks = sum(subject["marks"] for subject in cleaned_subjects)
    percentage = round(total_marks / total_subjects, 2)
    grade = grade_check(percentage)

    conn = get_db_connection()
    existing_student = conn.execute(
        "SELECT id FROM students WHERE id = ?",
        (st_id,),
    ).fetchone()

    if existing_student:
        conn.close()
        return jsonify({"error": "Student ID already exists"}), 400

    conn.execute(
        """
        INSERT INTO students
            (id, name, department, total_subjects, total_marks, percentage, grade)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (st_id, name, department, total_subjects, total_marks, percentage, grade),
    )

    conn.executemany(
        "INSERT INTO subjects (student_id, subject, marks) VALUES (?, ?, ?)",
        [
            (st_id, subject["subject"], subject["marks"])
            for subject in cleaned_subjects
        ],
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Student added successfully"}), 201


@app.route("/api/delete/<id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db_connection()
    student = conn.execute("SELECT id FROM students WHERE id = ?", (id,)).fetchone()

    if not student:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted successfully"}), 200


init_db()


if __name__ == "__main__":
    app.run(debug=True)
