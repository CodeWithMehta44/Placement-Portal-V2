from .utils import admin_required
from flask import Blueprint
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from database import db
from models.student import Student
from models.company import Company
from models.job_position import JobPosition
from models.application import Application

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/stats", methods=["GET"])
@jwt_required()
def dashboard_stats():

    return jsonify({
        "students": Student.query.count(),
        "companies": Company.query.count(),
        "jobs": JobPosition.query.count(),
        "applications": Application.query.count()
    }), 200

@admin_bp.route("/companies", methods=["GET"])
@admin_required
def get_companies():
    companies = Company.query.all()

    company_list = []

    for company in companies:
        company_list.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location,
            "is_approved": company.is_approved,
            "is_active": company.is_active
        })

    return jsonify(company_list), 200

@admin_bp.route("/students", methods=["GET"])
@admin_required
def get_students():

    students = Student.query.all()

    student_list = []

    for student in students:
        student_list.append({
            "id": student.id,
            "full_name": student.full_name,
            "college": student.college,
            "degree": student.degree,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "phone": student.phone,
            "is_active": student.is_active
        })

    return jsonify(student_list), 200

@admin_bp.route("/student/<int:student_id>/deactivate", methods=["PUT"])
@admin_required
def deactivate_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "error": "Student not found"
        }), 404

    student.is_active = False
    db.session.commit()

    return jsonify({
        "message": "Student deactivated successfully"
    }), 200

@admin_bp.route("/company/<int:company_id>/deactivate", methods=["PUT"])
@admin_required
def deactivate_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "error": "Company not found"
        }), 404

    company.is_active = False
    db.session.commit()

    return jsonify({
        "message": "Company deactivated successfully"
    }), 200


@admin_bp.route("/company/<int:company_id>/approve", methods=["PUT"])
@admin_required
def approve_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
        "error": "Company not found"
    }), 404
    company.is_approved = True

    db.session.commit()
    return jsonify({
        "message": "Company approved successfully"
    }), 200

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    return {
        "message": "Welcome Admin"
    }