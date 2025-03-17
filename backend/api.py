"""Functions that query the mathnasium database"""

from database_functions import (get_student_attendance, get_progress_check, get_checkup_data)
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def endpoint_index():
    """Sets up index route"""
    return jsonify({"message": "Welcome to the Mathnasium API"})

@app.route("/attendance", methods=["GET"])
def endpoint_get_attendance():
    """Returns students that have attended in a given period"""

    students = get_student_attendance()

    if students == []:
        return {"error": "Students not found"}, 404

    return jsonify(students), 200

@app.route("/progress_check", methods=["GET"])
def endpoint_get_progress_check():
    """Returns students that need a progress check"""

    students = get_progress_check()

    if students == []:
        return {"error": "Students not found"}, 404

    return jsonify(students), 200

@app.route("/checkup", methods=["GET"])
def endpoint_get_checkup():
    """Returns students that need a checkup"""

    students = get_checkup_data()

    if students == []:
        return {"error": "Students not found"}, 404

    return jsonify(students), 200

if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5000)