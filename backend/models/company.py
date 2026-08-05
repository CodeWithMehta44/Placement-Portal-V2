from database import db


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    company_name = db.Column(db.String(150), nullable=False)

    industry = db.Column(db.String(100))

    location = db.Column(db.String(150))

    website = db.Column(db.String(200))

    description = db.Column(db.Text)

    job_positions = db.relationship(
    "JobPosition",
    backref="company",
    lazy=True
)
    is_approved = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)