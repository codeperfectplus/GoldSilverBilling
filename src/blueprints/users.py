from datetime import datetime
from flask import render_template, request, redirect, url_for,  Blueprint, flash
from flask_bcrypt import generate_password_hash
from flask_login import  login_required, current_user

from src.config import db
from src.models import User, Settings

users_bp = Blueprint('users_', __name__)

@users_bp.route('/users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.user_level != 'admin':
        return redirect(url_for('additional.permission_denied'))
    users = User.query.all()
    return render_template('users/manage_users.html', users=users)

@users_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if current_user.user_level != 'admin':
        return redirect(url_for('additional.permission_denied'))
        
    if request.method == 'POST':
        user.fname = request.form['fname']
        user.lname = request.form['lname']
        user.username = request.form['username']
        user.email = request.form['email']
        user.user_level = request.form['user_level']
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('users_.manage_users'))
    return render_template('users/edit_user.html', user=user)

@users_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.user_level != 'admin':
        return redirect(url_for('additional.permission_denied'))
    if request.method == 'POST':
        new_user = User(
            fname=request.form['fname'],
            lname=request.form['lname'],
            username=request.form['username'],
            email=request.form['email'],
            password=generate_password_hash(request.form['password']),
            user_level=request.form['user_level']
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('users_.manage_users'))
    return render_template('users/create_user.html')

@users_bp.route('/users/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
        return redirect(url_for('users_.manage_users'))
    return render_template('users/delete_user.html', user=user)
