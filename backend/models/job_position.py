from database import db
from datetime import datetime


class JobPosition(db.Model):
    __tablename__ = "job_positions"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    salary = db.Column(db.Float)

    location = db.Column(db.String(150))

    skills_required = db.Column(db.Text)

    vacancies = db.Column(db.Integer)

    deadline = db.Column(db.Date)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    applications = db.relationship(
    "Application",
    backref="job_position",
    lazy=True
)