from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import db
from models.notification import Notification
from models.student import Student

notification_bp = Blueprint("notification", __name__)


@notification_bp.route("/student/notifications", methods=["GET"])
@jwt_required()
def get_notifications():

    user_id = get_jwt_identity()

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    notifications = Notification.query.filter_by(
        student_id=student.id
    ).order_by(Notification.created_at.desc()).all()

    data = []

    for notification in notifications:
        data.append({
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "created_at": notification.created_at,
            "is_read": notification.is_read
        })

    return jsonify(data), 200

@notification_bp.route("/student/notification/<int:id>/read", methods=["PUT"])
@jwt_required()
def mark_as_read(id):

    notification = Notification.query.get(id)

    if not notification:
        return jsonify({"message": "Notification not found"}), 404

    notification.is_read = True

    db.session.commit()

    return jsonify({
        "message": "Notification marked as read"
    }), 200