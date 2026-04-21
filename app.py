from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

DATA_FILE = "student.json"

# -------------------------
# Utility Functions
# -------------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def grade_check(percent):
    if percent >= 80: return "Distinction"
    elif percent >= 70: return "First Class"
    elif percent >= 60: return "Second Class"
    elif percent > 35: return "Pass"
    else: return "Fail"

# -------------------------
# Page Routes
# -------------------------

@app.route("/")
def index():
    return render_template("index.html")

# -------------------------
# API Routes
# -------------------------

@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify(load_data())

@app.route("/api/add", methods=["POST"])
def add_student():
    students = load_data()
    data = request.get_json()

    try:
        st_id = data.get("id")
        name = data.get("name")
        dept = data.get("department")
        subjects_list = data.get("subjects_list") # New dynamic list
        total_subjects = int(data.get("total_subjects"))
        total_marks = int(data.get("total_marks"))

        if st_id in students:
            return jsonify({"error": "Student ID already exists"}), 400

        # Dynamic Math: Average marks per subject
        # Formula: Total / Subjects (Assuming each subject is out of 100)
        percent = float(total_marks / total_subjects) if total_subjects > 0 else 0
        grade = grade_check(percent)

        students[st_id] = {
            "name": name,
            "department": dept,
            "subjects_list": subjects_list, # Store individual marks
            "no_sub": total_subjects,
            "Total_marks": total_marks,
            "Percentage": percent,
            "Grade": grade
        }

        save_data(students)
        return jsonify({"message": "Student added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/delete/<id>", methods=["DELETE"])
def delete_student(id):
    students = load_data()
    if id in students:
        del students[id]
        save_data(students)
        return jsonify({"message": "Deleted"}), 200
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)