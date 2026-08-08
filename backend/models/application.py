from database import db
from datetime import datetime


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("job_positions.id"),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Applied"
    )

    interview_date = db.Column(db.Date)
    interview_time = db.Column(db.Time)
    interview_location = db.Column(db.String(200))

    applied_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )