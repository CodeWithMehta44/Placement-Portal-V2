from .utils import admin_required
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

import os
from flask import send_file

from database import db
from models.application import Application
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

    search = request.args.get("search")

    query = Company.query

    if search:
        query = query.filter(
            db.or_(
                Company.company_name.ilike(f"%{search}%"),
                Company.industry.ilike(f"%{search}%")
            )
        )

    companies = query.all()

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

    search = request.args.get("search")

    query = Student.query

    if search:
        filters = [
            Student.full_name.ilike(f"%{search}%"),
            Student.phone.ilike(f"%{search}%")
        ]

        if search.isdigit():
            filters.append(Student.id == int(search))

        query = query.filter(db.or_(*filters))

    students = query.all()

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

@admin_bp.route("/jobs", methods=["GET"])
@admin_required
def get_jobs():

    jobs = JobPosition.query.all()

    job_list = []

    for job in jobs:
        job_list.append({
            "id": job.id,
            "company_id": job.company_id,
            "title": job.title,
            "salary": job.salary,
            "location": job.location,
            "vacancies": job.vacancies,
            "deadline": str(job.deadline),
            "created_at": str(job.created_at)
        })

    return jsonify(job_list), 200

@admin_bp.route("/job/<int:job_id>", methods=["DELETE"])
@admin_required
def delete_job(job_id):

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({
            "error": "Job not found"
        }), 404

    db.session.delete(job)
    db.session.commit()

    return jsonify({
        "message": "Job deleted successfully"
    }), 200



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

@admin_bp.route("/student/<int:student_id>/activate", methods=["PUT"])
@admin_required
def activate_student(student_id):

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "error": "Student not found"
        }), 404

    student.is_active = True
    db.session.commit()

    return jsonify({
        "message": "Student activated successfully"
    }), 200

@admin_bp.route("/company/<int:company_id>/activate", methods=["PUT"])
@admin_required
def activate_company(company_id):

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            "error": "Company not found"
        }), 404

    company.is_active = True
    db.session.commit()

    return jsonify({
        "message": "Company activated successfully"
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

@admin_bp.route("/applications", methods=["GET"])
@jwt_required()
def get_all_applications():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    applications = Application.query.all()

    data = []

    for application in applications:

        job = application.job_position
        student = application.student
        company = job.company

        data.append({
            "id": application.id,
            "student": student.full_name,
            "company": company.company_name,
            "job_title": job.title,
            "status": application.status,
            "applied_date": application.applied_date
        })

    return jsonify(data), 200


@admin_bp.route("/application/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_application(id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    application = Application.query.get(id)

    if not application:
        return jsonify({"error": "Application not found"}), 404

    db.session.delete(application)
    db.session.commit()

    return jsonify({
        "message": "Application deleted successfully"
    }), 200

@admin_bp.route("/reports/monthly", methods=["GET"])
@admin_required
def view_monthly_report():
    reports_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "reports"
    )

    if not os.path.exists(reports_dir):
        return jsonify({
            "error": "No reports available"
        }), 404

    reports = [
        file for file in os.listdir(reports_dir)
        if file.startswith("placement_report_") and file.endswith(".html")
    ]

    if not reports:
        return jsonify({
            "error": "No monthly report available"
        }), 404

    latest_report = max(
        reports,
        key=lambda file: os.path.getmtime(
            os.path.join(reports_dir, file)
        )
    )

    return send_file(
        os.path.join(reports_dir, latest_report)
    )