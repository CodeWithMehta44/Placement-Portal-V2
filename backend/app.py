from flask import Flask
from config import Config
from flask_jwt_extended import JWTManager
from database import db
from flask_cors import CORS

from models.user import User
from models.company import Company
from models.student import Student
from models.job_position import JobPosition
from models.application import Application
from models.placement import Placement

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.company import company_bp

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

jwt = JWTManager(app)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(company_bp, url_prefix="/company")

@app.route("/")
def home():
    return "Placement Portal API is Running!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)