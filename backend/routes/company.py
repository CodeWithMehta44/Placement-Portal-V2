from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import json
from cache import cache
from cache import clear_job_cache

import os
from flask import send_from_directory

from database import db
from models.job_position import JobPosition
from models.user import User
from models.company import Company
from models.application import Application
from models.student import Student
from models.notification import Notification

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

    clear_job_cache()

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

            "resume": student.resume

        })

    return jsonify(application_list), 200

@company_bp.route("/application/<int:application_id>/resume", methods=["GET"])
@jwt_required()
def view_application_resume(application_id):

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    application = Application.query.get(application_id)

    if not application:
        return jsonify({"error": "Application not found"}), 404

    job = JobPosition.query.get(application.job_id)

    if not job:
        return jsonify({"error": "Job not found"}), 404

    # Make sure this company owns the job
    if job.company_id != company.id:
        return jsonify({"error": "Unauthorized"}), 403

    student = Student.query.get(application.student_id)

    if not student or not student.resume:
        return jsonify({"error": "Resume not found"}), 404

    upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads",
        "resumes"
    )

    return send_from_directory(
        upload_folder,
        student.resume,
        as_attachment=False
    )

@company_bp.route("/application/<int:application_id>", methods=["PUT"])
@jwt_required()
def update_application_status(application_id):

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    application = Application.query.get(application_id)

    if not application:
        return jsonify({"error": "Application not found"}), 404

    job = JobPosition.query.get(application.job_id)

    if job.company_id != company.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    application.status = data["status"]

    status = application.status

    if status == "Shortlisted":
        title = "🎉 Application Shortlisted"
        message = f"Congratulations! You have been shortlisted for {job.title}."

    elif status == "Interview":
        title = "📅 Interview Scheduled"
        message = f"You have been invited for an interview for {job.title}."

    elif status == "Selected":
        title = "🥳 Congratulations!"
        message = f"You have been selected for {job.title}."

    elif status == "Rejected":
        title = "Update"
        message = f"Unfortunately, your application for {job.title} was not selected."

    else:
        title = "Application Updated"
        message = f"Your application status has changed to {status}."

    notification = Notification(
        student_id=application.student_id,
        title=title,
        message=message
    )

    db.session.add(notification)

    db.session.commit()

    return jsonify({
        "message": "Application updated successfully"
    }), 200

@company_bp.route("/job/<int:job_id>/status", methods=["PUT"])
@jwt_required()
def update_job_status(job_id):

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

    data = request.get_json()

    if "is_active" not in data:
        return jsonify({"error": "is_active is required"}), 400

    job.is_active = data["is_active"]

    db.session.commit()

    return jsonify({
        "message": "Job status updated successfully"
    }), 200

@company_bp.route("/application/<int:application_id>/interview", methods=["PUT"])
@jwt_required()
def schedule_interview(application_id):

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"error": "Company not found"}), 404

    application = Application.query.get(application_id)

    if not application:
        return jsonify({"error": "Application not found"}), 404

    job = JobPosition.query.get(application.job_id)

    if job.company_id != company.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    application.interview_date = datetime.strptime(
        data["interview_date"],
        "%Y-%m-%d"
    ).date()

    application.interview_time = datetime.strptime(
        data["interview_time"],
        "%H:%M"
    ).time()

    application.interview_location = data["interview_location"]

    application.status = "Interview"

    db.session.commit()

    return jsonify({
        "message": "Interview scheduled successfully"
    }), 200

@company_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_company_profile():
    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    user = User.query.get(user_id)

    return jsonify({
        "company_name": company.company_name,
        "email": user.email,
        "industry": company.industry,
        "website": company.website,
        "location": company.location,
        "description": company.description
    }), 200

@company_bp.route("/search", methods=["GET"])
@jwt_required()
def search_companies():

    search = request.args.get("search", "").strip()

    cache_key = f"companies:{search.lower()}"

    # Check Redis cache
    cached_data = cache.get(cache_key)

    if cached_data:
        print("COMPANY CACHE HIT")
        return jsonify(json.loads(cached_data)), 200

    print("COMPANY CACHE MISS")

    # Search companies from database
    query = Company.query

    if search:
        query = query.filter(
            Company.company_name.ilike(f"%{search}%")
        )

    companies = query.all()

    company_list = []

    for company in companies:
        company_list.append({
            "id": company.id,
            "company_name": company.company_name
        })

    # Store result in Redis for 60 seconds
    cache.set(
        cache_key,
        json.dumps(company_list),
        ex=60
    )

    print("COMPANY CACHE STORED")

    return jsonify(company_list), 200