from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import db
from models.company import Company
from models.application import Application
from models.job_position import JobPosition
from models.student import Student

student_bp = Blueprint("student", __name__)

@student_bp.route("/jobs", methods=["GET"])
@jwt_required()
def get_available_jobs():

    jobs = db.session.query(JobPosition, Company).join(
        Company,
        JobPosition.company_id == Company.id
    ).filter(
        Company.is_approved == True,
        Company.is_active == True,
        JobPosition.is_active == True
    ).all()

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
            "company": company.company_name,
            "title": job.title,
            "status": application.status,
            "applied_date": str(application.applied_date)
        })

    return jsonify(application_list), 200