from datetime import datetime

from flask import render_template, Blueprint

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health():
    health_info = {
        "status": "healthy",
        "message": "The server is up and running.",
        "version": "2.0.1",
        "timestamp": datetime.now().isoformat()
    }
    return render_template('others/health.html', **health_info)