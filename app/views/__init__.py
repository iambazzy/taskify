from flask import Blueprint, jsonify
from .auth import auth_bp
from .tasks import tasks_bp
main_bp = Blueprint('main_bp', __name__)
main_bp.register_blueprint(auth_bp)
main_bp.register_blueprint(tasks_bp)


@main_bp.route('/')
def server_health():
    return jsonify(status='ok')
