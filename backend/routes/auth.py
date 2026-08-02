from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data provided"
        }), 400

    required_fields = ["name", "email", "password"]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({
            "error": "Email already registered"
        }), 409

    user = User(
        name=data["name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role="student"
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Student Registered Successfully"
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
        "error": "No data provided"
        }), 400

    required_fields = ["email", "password"]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    if not check_password_hash(user.password, data["password"]):
        return jsonify({
            "error": "Invalid email or password"
    }), 401

    return jsonify({
    "message": "Login Successful",
    "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }
}), 200