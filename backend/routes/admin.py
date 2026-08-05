from .utils import admin_required
from flask import Blueprint

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    return {
        "message": "Welcome Admin"
    }