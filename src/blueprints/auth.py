from datetime import datetime, timezone
from flask import render_template, request, redirect, url_for,  Blueprint, flash

from flask_login import login_user, logout_user, current_user, login_required

from src.config import app, db, bcrypt, login_manager
from src.models import User, log_action, Settings

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        # Check if this is the first user
        if User.query.count() == 0:
            user_level = 'admin'  # Make the first user an admin
            password_changed = False
        else:
            user_level = 'customer'  # Default to 'customer' for all other users
            password_changed = True
        user = User(fname=fname, lname=lname, username=username, email=email, password=password, user_level=user_level, password_changed=password_changed)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('admin/register.html')

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    system_settings = Settings.query.first()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            log_action(user.id, user.username, 'Login', f'User {user.username} logged in.')

            flash(f'Login successful as {user.username}', 'success')
            return redirect(url_for('admin_.dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('admin/login.html', settings=system_settings)

@auth_bp.route("/change-password", methods=['GET', 'POST'])
@login_required
def change_password():
    system_settings = Settings.query.first()
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        user = User.query.get(current_user.id)

        if user and bcrypt.check_password_hash(user.password, current_password):
            user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password_changed = True  # Set the flag to True
            user.last_password_change=datetime.now(timezone.utc)
            db.session.commit()
            flash('Password updated successfully!', 'success')

            return redirect(url_for('auth.change_password'))
        else:
            flash('Current password is incorrect.', 'danger')

    # if current user password_changed false, flash a message
    if not current_user.password_changed:
        flash('Password needs to be changed first time login', 'danger')
        return render_template('admin/change_password.html', settings=system_settings)

    return render_template('admin/change_password.html', settings=system_settings)
        

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
