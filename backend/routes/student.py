from flask import Blueprint,request,jsonify,send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity

import os
from werkzeug.utils import secure_filename

from database import db
from models.company import Company
from models.application import Application
from models.job_position import JobPosition
from models.student import Student
from models.user import User

student_bp = Blueprint("student", __name__)

UPLOAD_FOLDER = "uploads/resumes"
ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@student_bp.route("/jobs", methods=["GET"])
@jwt_required()
def get_available_jobs():

    search = request.args.get("search", "").strip()

    query = db.session.query(JobPosition, Company).join(
    Company,
    JobPosition.company_id == Company.id
    ).filter(
        Company.is_approved == True,
        Company.is_active == True,
        JobPosition.is_active == True
    )

    if search:
        query = query.filter(
            db.or_(
                JobPosition.title.ilike(f"%{search}%"),
                JobPosition.skills_required.ilike(f"%{search}%"),
                JobPosition.location.ilike(f"%{search}%"),
                Company.company_name.ilike(f"%{search}%")
            )
        )

    jobs = query.all()

    job_list = []

    for job, company in jobs:

        job_list.append({
            "id": job.id,
            "company": company.company_name,
            "title": job.title,
            "salary": job.salary,
            "location": job.location,
            "deadline": str(job.deadline)
        })

    return jsonify(job_list), 200

@student_bp.route("/job/<int:job_id>", methods=["GET"])
@jwt_required()
def get_job_details(job_id):

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({
            "error": "Job not found"
        }), 404

    company = Company.query.get(job.company_id)

    return jsonify({
        "id": job.id,
        "company": company.company_name,
        "title": job.title,
        "description": job.description,
        "salary": job.salary,
        "location": job.location,
        "skills_required": job.skills_required,
        "deadline": str(job.deadline)
    }), 200

@student_bp.route("/job/<int:job_id>/apply", methods=["POST"])
@jwt_required()
def apply_job(job_id):

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({
            "error": "Student not found"
        }), 404

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({
            "error": "Job not found"
        }), 404

    existing = Application.query.filter_by(
        student_id=student.id,
        job_id=job.id
    ).first()

    if existing:
        return jsonify({
            "error": "Already applied"
        }), 400

    application = Application(
        student_id=student.id,
        job_id=job.id,
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({
        "message": "Applied Successfully"
    }), 201

@student_bp.route("/job/<int:job_id>/status", methods=["GET"])
@jwt_required()
def application_status(job_id):

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({
            "error": "Student not found"
        }), 404

    application = Application.query.filter_by(
        student_id=student.id,
        job_id=job_id
    ).first()

    if application:
        return jsonify({
            "applied": True,
            "status": application.status
        }), 200

    return jsonify({
        "applied": False
    }), 200

@student_bp.route("/applications", methods=["GET"])
@jwt_required()
def get_my_applications():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({
            "error": "Student not found"
        }), 404

    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    application_list = []

    for application in applications:

        job = application.job_position
        company = job.company

        application_list.append({
            "id": application.id,
            "job_id": job.id,
            "company": company.company_name,
            "title": job.title,
            "status": application.status,
            "applied_date": str(application.applied_date),

            "interview_date": str(application.interview_date) if application.interview_date else None,
            "interview_time": str(application.interview_time) if application.interview_time else None,
            "interview_location": application.interview_location
        })

    return jsonify(application_list), 200

@student_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    user = User.query.get(user_id)

    return jsonify({
        "full_name": student.full_name,
        "email": user.email,
        "college": student.college,
        "degree": student.degree,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "graduation_year": student.graduation_year,
        "skills": student.skills,
        "phone": student.phone,
        "linkedin": student.linkedin,
        "github": student.github,
        "resume": student.resume
    }), 200

@student_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()

    student.full_name = data.get("full_name", student.full_name)
    student.college = data.get("college", student.college)
    student.degree = data.get("degree", student.degree)
    student.branch = data.get("branch", student.branch)
    student.cgpa = data.get("cgpa", student.cgpa)
    student.graduation_year = data.get("graduation_year", student.graduation_year)
    student.skills = data.get("skills", student.skills)
    student.phone = data.get("phone", student.phone)
    student.linkedin = data.get("linkedin", student.linkedin)
    student.github = data.get("github", student.github)
    student.resume = data.get("resume", student.resume)

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200
# Resumee...
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@student_bp.route("/profile/resume", methods=["POST"])
@jwt_required()
def upload_resume():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    if "resume" not in request.files:
        return jsonify({
            "message": "No resume file provided"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "message": "No file selected"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "message": "Only PDF files are allowed"
        }), 400

    filename = secure_filename(file.filename)

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(file_path)

    student.resume = filename

    db.session.commit()

    return jsonify({
        "message": "Resume uploaded successfully",
        "resume": filename
    }), 200