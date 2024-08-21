from flask import render_template, Blueprint


additional_bp = Blueprint('additional', __name__)

@additional_bp.route('/pricing')
def pricing() -> str:
    return render_template('others/pricing.html')

@additional_bp.route('/features')
def features() -> str:
    return render_template('others/features.html')

@additional_bp.route('/about')
def about() -> str:
    return render_template('others/about.html')

@additional_bp.route('/permission-denied')
def permission_denied():
    return render_template('others/permission_denied.html')
