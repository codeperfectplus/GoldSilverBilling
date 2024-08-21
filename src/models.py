from datetime import datetime, timezone
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from src.config import db, app

class GoldTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    price_per_gram = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    purity = db.Column(db.String(50), nullable=False)
    service_charge = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    tax = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    total = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class SilverTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    price_per_gram = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    purity = db.Column(db.String(50), nullable=False)
    service_charge = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    tax = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    total = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    last_password_change = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_level = db.Column(db.String(20), nullable=False, default='customer')
    password_changed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.user_level}')"

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10), nullable=False)
    theme = db.Column(db.String(10), nullable=False)
    language = db.Column(db.String(20), nullable=False)
    is_flash_message_enabled = db.Column(db.Boolean, default=False)
    flash_message_timeout = db.Column(db.Integer, nullable=False, default=5)
    is_gold_jewellers_sidebar = db.Column(db.Boolean, default=False)
    is_gold_calculator_enabled = db.Column(db.Boolean, default=False)
    is_silver_calculator_enabled = db.Column(db.Boolean, default=False)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    details = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"AuditLog('{self.user_id}', '{self.action}', '{self.timestamp}')"

class JewellerDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jeweller_name = db.Column(db.String(100), nullable=False)
    jeweller_address = db.Column(db.String(255), nullable=False)
    jeweller_contact = db.Column(db.String(20), nullable=False)
    jeweller_email = db.Column(db.String(100), nullable=False)
    jeweller_website = db.Column(db.String(100), nullable=False)
    jeweller_gstin = db.Column(db.String(15), nullable=False)
    gold_price_per_gram = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    jeweller_logo = db.Column(db.String(255), nullable=True)

def initialize_database():
    with app.app_context():
        # Create tables
        db.create_all()

        # Initialize settings if not exists
        if not Settings.query.first():
            default_settings = Settings(
                currency='INR',
                theme='light',
                language='en',
                is_flash_message_enabled=True,
                flash_message_timeout=5,
                is_gold_jewellers_sidebar=True,
                is_gold_calculator_enabled=True,
                is_silver_calculator_enabled=True
            )
            db.session.add(default_settings)
            db.session.commit()

        # Initialize jeweller details if not exists
        if not JewellerDetails.query.first():
            default_jeweller_details = JewellerDetails(
                jeweller_name='GoldSilverBilling',
                jeweller_address='123, Main Street, City, Country',
                jeweller_contact='1234567890',
                jeweller_email='info@goldsilverbilling.com',
                jeweller_website='https://goldsilverbilling.com',
                jeweller_gstin='ABC1234567890',
                gold_price_per_gram=5000.00,
                jeweller_logo='images/logo.png'
            )
            db.session.add(default_jeweller_details)
            db.session.commit()

        # Initialize users if not exists
        user_data_list = [
            {
                'fname': 'Admin',
                'lname': 'User',
                'username': 'admin',
                'email': 'admin@gmail.com',
                'password': generate_password_hash('admin'),
                'user_level': 'admin',
                'last_password_change': datetime.now(timezone.utc)
            },
            {
                'fname': 'Customer',
                'lname': 'User',
                'username': 'customer',
                'email': 'customer@gmail.com',
                'password': generate_password_hash('customer'),
                'user_level': 'customer',
                'last_password_change': datetime.now(timezone.utc)
            }
        ]

        for user_data in user_data_list:
            if not User.query.filter_by(username=user_data['username']).first():
                user = User(**user_data)
                db.session.add(user)
                db.session.commit()
                print(f"{user_data['username']} user created successfully.")
            else:
                print(f"{user_data['username']} user already exists.")

def log_action(user_id, username, action, details=None):
    if isinstance(details, list):
        details = '<br>'.join(details)
    
    log_entry = AuditLog(
        user_id=user_id, 
        username=username, 
        action=action, 
        details=details
    )
    db.session.add(log_entry)
    db.session.commit()
