from flask import Flask
from config import Config
from database import db

from models.user import User
from models.company import Company
from models.student import Student
from models.job_position import JobPosition
from models.application import Application
from models.placement import Placement

from routes.auth import auth_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return "Placement Portal API is Running!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)