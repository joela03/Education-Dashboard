"""Functions that query the mathnasium database"""

from dotenv import load_dotenv
import os
from database_functions import (get_student_attendance, get_progress_check, get_checkup_data,
                                get_plan_pace, get_username_data)
from imports import verify_password
from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import BaseModel
import jwt
from datetime import datetime

load_dotenv()
JWT_KEY = os.getenv("JWT_KEY")

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def endpoint_index():
    """Sets up index route"""
    return jsonify({"message": "Welcome to the Mathnasium API"})

class LoginRequest(BaseModel):
    username: str
    password: str

@app.route("/login", methods=["POST"])
def login():
    """Verifies that user password_hash matches the associated one"""

    try:
        data = request.get_json()
        
        if not data or "username" not in data or "password" not in data:
            return jsonify({"error": "Missing username or password"}), 400
        
        username = data.get("username")
        
        try:
            user = get_username_data(username)
        except Exception as e:
            return jsonify({"error": "Error retrieving user data", "details": str(e)}), 500
        
        if not user or not verify_password(user.get("salt"), user.get("password_hash"), data.get("password")):
            return jsonify({"error": "Invalid credentials"}), 401
        
        payload = {
            "sub": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_KEY, algorithm="HS256")

        return jsonify({"access_token": token, "token_type": "bearer"})
    
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

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

@app.route("/planpace", methods=["GET"])
def endpoint_get_planpace():
    """Returns students that are progressing at less than the expect plan pace"""

    students = get_plan_pace()

    if students == []:
        return {"error": "Students not found"}, 404

    return jsonify(students), 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5000)