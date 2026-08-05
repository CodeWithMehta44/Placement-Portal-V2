from app import app
from database import db
from models.user import User
from werkzeug.security import generate_password_hash

with app.app_context():

    admin = User.query.filter_by(email="admin@portal.com").first()

    if not admin:
        admin = User(
            name="Admin",
            email="admin@portal.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin Created Successfully")

    else:
        print("Admin Already Exists")