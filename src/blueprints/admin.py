import psutil

from flask import render_template, request, session, redirect, url_for, flash, Blueprint

from flask_login import current_user, login_required
from flask_login import current_user, login_required

from src.config import db
from src.models import User, AuditLog, Settings, log_action

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.user_level != 'admin':
        return redirect(url_for('permission_denied'))

    users = User.query.all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_level = request.form.get('user_level')
        
        user = User.query.get(user_id)
        if user:
            user.user_level = new_level
            db.session.commit()
            flash(f"User {user.username}'s level updated to {new_level}.", 'success')
        else:
            flash("User not found.", 'error')

    return render_template('manage_users.html', users=users)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if current_user.user_level != 'admin':
        return redirect(url_for('home'))

    if request.method == 'POST':
        currency = request.form.get('currency')
        theme = request.form.get('theme')
        language = request.form.get('language')
        is_gold_jewellers_sidebar = int(request.form.get('is_gold_jewellers_sidebar'))
        is_gold_calculator_enabled = int(request.form.get('is_gold_calculator_enabled'))
        is_silver_calculator_enabled = int(request.form.get('is_silver_calculator_enabled'))

        # Save the settings (you might save them to a database or a config file)
        # Assuming you have a Settings model or similar logic to save settings
        settings = Settings.query.first()
        if not settings:
            settings = Settings(currency=currency, theme=theme, language=language,
                                is_gold_jewellers_sidebar=is_gold_jewellers_sidebar,
                                is_gold_calculator_enabled=is_gold_calculator_enabled,
                                is_silver_calculator_enabled=is_silver_calculator_enabled)
        else:
            settings.currency = currency
            settings.theme = theme
            settings.language = language
            settings.is_gold_jewellers_sidebar = is_gold_jewellers_sidebar
            settings.is_gold_calculator_enabled = is_gold_calculator_enabled
            settings.is_silver_calculator_enabled = is_silver_calculator_enabled

        db.session.add(settings)
        db.session.commit()
        
        log_action(current_user.id, current_user.username, 'System Settings Change', details=f"Currency set to {currency}, Theme set to {theme}")
        return redirect(url_for('settings'))
    
    settings = Settings.query.first()
    return render_template('settings.html', settings=settings)


@admin_bp.route('/admin/audit_log')
@login_required
def audit_log():
    if current_user.user_level != 'admin':
        return redirect(url_for('home'))

    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template('audit_log.html', logs=logs)


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.user_level == 'admin':
        total_users = User.query.count()  # Count total users
        active_sessions = len(session)  # This is a basic approach. You may want to track sessions differently.
        
        # Example: If you store active users in the session, you might track like this:
        active_sessions = session.get('active_users', 0)
        
        system_health = "Good"  # This can be determined by your own logic
        cpu_core = psutil.cpu_count()
        cpu_utilization = psutil.cpu_percent(interval=1)

        if cpu_utilization > 80:
            system_health = "Warning"
        else:
            system_health = "Good"

        audit_logs = AuditLog.query.filter_by(user_id=current_user.id).all()
        return render_template('admin_dashboard.html', 
                            total_users=total_users, 
                            active_sessions=active_sessions, 
                            system_health=system_health,
                            cpu_core=cpu_core,
                            cpu_util=cpu_utilization,
                            audit_logs=audit_logs)
    elif current_user.user_level == 'customer':
        audit_logs = AuditLog.query.filter_by(user_id=current_user.id).all()
        return render_template('customer_dashboard.html', audit_logs=audit_logs)
 

