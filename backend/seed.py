from app import app
from database import db
from models.user import User

with app.app_context():

    admin = User.query.filter_by(email="admin@placement.com").first()

    if not admin:
        admin = User(
            name="Admin",
            email="admin@placement.com",
            password="admin123",
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully!")

    else:
        print("Admin already exists!")