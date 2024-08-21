import os
from flask import Flask, render_template
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize the Flask app
app = Flask(__name__)

# Load configuration from environment variables or fallback to defaults
app.secret_key = os.getenv('SECRET_KEY', 'jhd87^&*^udhwduy792ejlndhy783uh')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///production.db' # commit this to git
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['INITIALIZED'] = False

Session(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('others/404.html'), 404


# Custom filter to format dates
@app.template_filter('format_datetime')
def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    if value is not None:
        return value.strftime(format)
    return ''
