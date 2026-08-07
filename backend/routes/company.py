from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from database import db
from models.job_position import JobPosition
from models.user import User
from models.company import Company
from models.application import Application
from models.student import Student

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

@company_bp.route("/job", methods=["POST"])
@jwt_required()
def create_job():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({
            "error": "Company not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data provided"
        }), 400

    required_fields = [
        "title",
        "description",
        "salary",
        "location",
        "skills_required",
        "vacancies",
        "deadline"
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    job = JobPosition(
        company_id=company.id,
        title=data["title"],
        description=data["description"],
        salary=data["salary"],
        location=data["location"],
        skills_required=data["skills_required"],
        vacancies=data["vacancies"],
        deadline=datetime.strptime(
            data["deadline"],
            "%Y-%m-%d"
        ).date()
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({
        "message": "Job created successfully"
    }), 201

@company_bp.route("/stats", methods=["GET"])
@jwt_required()
def company_stats():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({
            "error": "Company not found"
        }), 404

    total_jobs = JobPosition.query.filter_by(company_id=company.id).count()

    active_jobs = JobPosition.query.filter_by(
        company_id=company.id,
        is_active=True
    ).count()

    total_applications = Application.query.join(JobPosition).filter(
        JobPosition.company_id == company.id
    ).count()

    shortlisted = Application.query.join(JobPosition).filter(
        JobPosition.company_id == company.id,
        Application.status == "Shortlisted"
    ).count()

    return jsonify({
        "totalJobs": total_jobs,
        "activeJobs": active_jobs,
        "applications": total_applications,
        "shortlisted": shortlisted
    }), 200

@company_bp.route("/jobs", methods=["GET"])
@jwt_required()
def get_company_jobs():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({
            "error": "Company not found"
        }), 404

    jobs = JobPosition.query.filter_by(company_id=company.id).all()

    job_list = []

    for job in jobs:
        job_list.append({
            "id": job.id,
            "title": job.title,
            "salary": job.salary,
            "deadline": str(job.deadline),
            "is_active": job.is_active
        })

    return jsonify(job_list), 200

@company_bp.route("/job/<int:job_id>", methods=["GET"])
@jwt_required()
def get_job(job_id):

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    job = JobPosition.query.filter_by(
        id=job_id,
        company_id=company.id
    ).first()

    if not job:
        return jsonify({"error": "Job not found"}), 404

    return jsonify({
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "salary": job.salary,
        "location": job.location,
        "deadline": str(job.deadline),
        "skills_required": job.skills_required,
        "vacancies": job.vacancies,
        "is_active": job.is_active
    }), 200

@company_bp.route("/job/<int:job_id>/applications", methods=["GET"])
@jwt_required()
def get_job_applications(job_id):

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    job = JobPosition.query.filter_by(
        id=job_id,
        company_id=company.id
    ).first()

    if not job:
        return jsonify({"error": "Job not found"}), 404

    applications = Application.query.filter_by(job_id=job.id).all()

    application_list = []

    for application in applications:

        student = Student.query.get(application.student_id)

        application_list.append({

            "application_id": application.id,

            "student_name": student.full_name,

            "cgpa": student.cgpa,

            "status": application.status,

            "resume_url": student.resume_url

        })

    return jsonify(application_list), 200