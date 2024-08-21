from flask import flash, render_template
from flask_login import current_user
from src.config import db
from src.models import Settings

def require_password_change(func):
    def wrapper(*args, **kwargs):
        # Check if the user is authenticated and if a password change is required
        if current_user.is_authenticated and not current_user.password_changed:
            flash('You need to change your password first to continue.', 'warning')
            system_settings = Settings.query.first()  # Ensure to load system settings if needed
            return render_template('change_password.html', settings=system_settings)
        return func(*args, **kwargs)
    return wrapper
