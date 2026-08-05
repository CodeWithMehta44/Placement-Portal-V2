from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from database import db
from models.user import User
from models.company import Company

company_bp = Blueprint("company", __name__)


@company_bp.route("/register", methods=["POST"])
def register_company():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data provided"
        }), 400

    required_fields = [
        "company_name",
        "industry",
        "location",
        "email",
        "password"
    ]

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

    # Create login account
    user = User(
        name=data["company_name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role="company"
    )

    db.session.add(user)
    db.session.commit()

    # Create company profile
    company = Company(
        user_id=user.id,
        company_name=data["company_name"],
        industry=data["industry"],
        location=data["location"],
        website=data.get("website"),
        description=data.get("description")
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({
        "message": "Company registered successfully. Waiting for admin approval."
    }), 201