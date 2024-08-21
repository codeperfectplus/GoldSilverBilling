
from flask import render_template, request, redirect, url_for,  Blueprint

from flask_login import login_user, logout_user

from src.config import app, db, bcrypt, login_manager
from src.models import User, log_action

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
        else:
            user_level = 'customer'  # Default to 'customer' for all other users
        user = User(fname=fname, lname=lname, username=username, email=email, password=password, user_level=user_level)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            log_action(user.id, user.username, 'Login', f'User {user.username} logged in.')
            return redirect(url_for('admin.dashboard'))
    return render_template('login.html')

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

