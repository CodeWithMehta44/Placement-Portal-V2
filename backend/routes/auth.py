from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)

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

    access_token = create_access_token(
    identity=str(user.id),
    additional_claims={
        "role": user.role,
        "email": user.email
    }
)

    return jsonify({
        "message": "Login Successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    claims = get_jwt()

    return jsonify({
        "message": "Protected Route",
        "email": claims["email"],
        "role": claims["role"]
    }), 200