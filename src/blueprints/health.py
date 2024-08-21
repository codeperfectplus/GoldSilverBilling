from datetime import datetime

from flask import render_template, Blueprint

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health():
    health_info = {
        "status": "healthy",
        "message": "The server is up and running.",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }
    return render_template('health.html', **health_info)