from datetime import datetime
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

from config import db, app

class GoldTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    price_per_gram = db.Column(db.Float, nullable=False)
    purity = db.Column(db.String(50), nullable=False)
    service_charge = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class SilverTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    price_per_gram = db.Column(db.Float, nullable=False)
    purity = db.Column(db.String(50), nullable=False)
    service_charge = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_level = db.Column(db.String(10), nullable=False, default='customer')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.user_level}')"


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10), nullable=False)
    theme = db.Column(db.String(10), nullable=False)
    language = db.Column(db.String(15), nullable=False)
    is_gold_jewellers_sidebar = db.Column(db.Boolean, default=False)
    is_gold_calculator_enabled = db.Column(db.Boolean, default=False)
    is_silver_calculator_enabled = db.Column(db.Boolean, default=False)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"AuditLog('{self.user_id}', '{self.action}', '{self.timestamp}')"

class JewellerDetails(db.Model):
    __tablename__ = 'jeweller_details'
    id = db.Column(db.Integer, primary_key=True)
    jeweller_name = db.Column(db.String(100), nullable=False)
    jeweller_address = db.Column(db.String(255), nullable=False)
    jeweller_contact = db.Column(db.String(15), nullable=False)
    jeweller_email = db.Column(db.String(100), nullable=False)
    jeweller_website = db.Column(db.String(100), nullable=False)
    jeweller_gstin = db.Column(db.String(15), nullable=False)
    gold_price_per_gram = db.Column(db.Float, nullable=False)
    jeweller_logo = db.Column(db.String(255), nullable=True)

    def __init__(self, jeweller_name, jeweller_address, jeweller_contact, jeweller_email, jeweller_website, jeweller_gstin, gold_price_per_gram, jeweller_logo):
        self.jeweller_name = jeweller_name
        self.jeweller_address = jeweller_address
        self.jeweller_contact = jeweller_contact
        self.jeweller_email = jeweller_email
        self.jeweller_website = jeweller_website
        self.jeweller_gstin = jeweller_gstin
        self.gold_price_per_gram = gold_price_per_gram
        self.jeweller_logo = jeweller_logo

# Create the database
with app.app_context():
    db.create_all()


# first commit in database for settings
with app.app_context():
    if not Settings.query.first():
        settings = Settings(currency='INR', theme='light', language='en',
                            is_gold_jewellers_sidebar=True,
                            is_gold_calculator_enabled=True, 
                            is_silver_calculator_enabled=True)
        db.session.add(settings)
        db.session.commit()

# initial commit in database for jeweller_details
with app.app_context():
    if not JewellerDetails.query.first():
        jeweller_details = JewellerDetails(
            jeweller_name='GoldSilverBilling',
            jeweller_address='123, Main Street, City, Country',
            jeweller_contact='1234567890',
            jeweller_email='info@goldsilverbilling.com',
            jeweller_website='https://goldsilverbilling.com',
            jeweller_gstin='ABC1234567890',
            gold_price_per_gram=5000.00,
            jeweller_logo='images/logo.png')
        db.session.add(jeweller_details)
        db.session.commit()

# create a initial admin user
with app.app_context():
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            fname='Admin',
            lname='User',
            username='admin',
            email='admin@gmail.com',
            password=generate_password_hash('admin'),
            user_level='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")
