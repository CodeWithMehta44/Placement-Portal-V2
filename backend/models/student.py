from database import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    full_name = db.Column(db.String(150), nullable=False)

    college = db.Column(db.String(150))

    degree = db.Column(db.String(100))

    branch = db.Column(db.String(100))

    cgpa = db.Column(db.Float)

    graduation_year = db.Column(db.Integer)

    skills = db.Column(db.Text)

    resume = db.Column(db.String(255))

    phone = db.Column(db.String(20))

    linkedin = db.Column(db.String(255))

    github = db.Column(db.String(255))

    applications = db.relationship(
    "Application",
    backref="student",
    lazy=True
    )

    placements = db.relationship(
    "Placement",
    backref="student",
    lazy=True
)
    