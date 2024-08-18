import os
import json
import logging 
import csv
from io import StringIO, BytesIO
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, send_file
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from calcualtors import GoldCalculator, SilverCalculator

# Initialize the Flask app
app = Flask(__name__)

# Load configuration from environment variables or fallback to defaults
app.secret_key = os.getenv('SECRET_KEY', 'jhd87^&*^udhwduy792ejlndhy783uh')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Session(app)
db = SQLAlchemy(app)

# Load configuration from JSON file
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, 'config.json')

def load_config() -> dict:
    """Loads configuration from a JSON file."""
    try:
        with open(CONFIG_FILE_PATH) as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found at {CONFIG_FILE_PATH}")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON config: {e}")
        return {}

app.config.update(load_config())

# Define the database models
class GoldTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    price_per_gram = db.Column(db.Float, nullable=False)
    purity = db.Column(db.String(50), nullable=False)
    service_charge = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class SilverTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    price_per_gram = db.Column(db.Float, nullable=False)
    purity = db.Column(db.String(50), nullable=False)
    service_charge = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database
with app.app_context():
    db.create_all()

# Health check endpoint
@app.route('/health', methods=['GET'])
def health() -> jsonify:
    return jsonify({
        "status": "healthy",
        "message": "The server is up and running.",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

# Home route
@app.route('/')
def home() -> str:
    return render_template('homepage.html')

# Gold calculator route
@app.route('/gold-calculator', methods=['GET', 'POST'])
def gold_calculator():
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            gold_price_per_gram = float(request.form['price_per_gram'])
            gold_service_charge = float(request.form['service_charge'])
            gold_tax = float(request.form['tax'])
            purity = request.form['purity']

            # Save price per gram to session
            session['gold_price_per_gram'] = gold_price_per_gram
            session['gold_service_charge'] = gold_service_charge
            session['gold_tax'] = gold_tax

            # Calculate gold price
            gold_item = GoldCalculator(weight, gold_price_per_gram, gold_service_charge, gold_tax)
            bill_details = gold_item.calculate_price()

            # Save to database
            transaction = GoldTransaction(
                weight=weight,
                price_per_gram=gold_price_per_gram,
                purity=purity,
                service_charge=gold_service_charge,
                tax=gold_tax,
                total=bill_details['Final Price']
            )
            db.session.add(transaction)
            db.session.commit()

            return render_template('gold_bill.html',
                                   bill=bill_details,
                                   weight=weight,
                                   price_per_gram=gold_price_per_gram,
                                   purity=purity,
                                   config=app.config)
        except ValueError as e:
            logging.error(f"ValueError in gold calculator: {str(e)}")
            flash(f"Input error: {str(e)}", 'error')
            return redirect(url_for('gold_calculator'))

    # Use session-stored price per gram or a default value
    gold_price_per_gram = session.get('gold_price_per_gram', 0)
    gold_service_charge = session.get('gold_service_charge', 0)
    gold_tax = session.get('gold_tax', 0)

    return render_template('gold_calculator.html',
                           price_per_gram=gold_price_per_gram,
                           service_charge=gold_service_charge,
                           tax=gold_tax,
                           config=app.config)

# Silver calculator route
@app.route('/silver-calculator', methods=['GET', 'POST'])
def silver_calculator():
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            silver_price_per_gram = float(request.form['price_per_gram'])
            silver_purity = float(request.form['purity'])
            silver_service_charge = float(request.form['service_charge'])
            silver_tax = float(request.form['tax'])

            # Save price per gram to session
            session['silver_price_per_gram'] = silver_price_per_gram
            session['silver_service_charge'] = silver_service_charge
            session['silver_tax'] = silver_tax

            # Calculate silver price
            silver_item = SilverCalculator(
                weight=weight,
                price_per_gram=silver_price_per_gram,
                service_charge=silver_service_charge,
                tax=silver_tax,
                purity=silver_purity
            )
            bill_details = silver_item.calculate_price()

            # Save to database
            transaction = SilverTransaction(
                weight=weight,
                price_per_gram=silver_price_per_gram,
                service_charge=silver_service_charge,
                tax=silver_tax,
                total=bill_details['Final Price'],
                purity=silver_purity
            )
            db.session.add(transaction)
            db.session.commit()

            return render_template('silver_bill.html',
                                   bill=bill_details,
                                   weight=weight,
                                   price_per_gram=silver_price_per_gram,
                                   purity=silver_purity,
                                   config=app.config)
        except ValueError as e:
            logging.error(f"ValueError in silver calculator: {str(e)}")
            flash(f"Input error: {str(e)}", 'error')
            return redirect(url_for('silver_calculator'))

    # Use session-stored price per gram or a default value
    silver_price_per_gram = session.get('silver_price_per_gram', 0)
    silver_service_charge = session.get('silver_service_charge', 0)
    silver_tax = session.get('silver_tax', 0)

    return render_template('silver_calculator.html',
                           price_per_gram=silver_price_per_gram,
                           service_charge=silver_service_charge,
                           tax=silver_tax,
                           config=app.config)

@app.route('/history', methods=['GET'])
def history():
    selected_type = request.args.get('type', 'all')

    if selected_type == 'gold':
        transactions = GoldTransaction.query.all()
        transactions = [{'id': t.id, 'type': 'Gold', 'weight': t.weight, 'price_per_gram': t.price_per_gram, 
                         "purity": t.purity, 'service_charge': t.service_charge, 'tax': t.tax, 'total': t.total, 'timestamp': t.timestamp} for t in transactions]
    elif selected_type == 'silver':
        transactions = SilverTransaction.query.all()
        transactions = [{'id': t.id, 'type': 'Silver', 'weight': t.weight, 'price_per_gram': t.price_per_gram,
                         'purity': t.purity, 'service_charge': t.service_charge, 'tax': t.tax, 'total': t.total, 'timestamp': t.timestamp} for t in transactions]
    else:
        gold_transactions = GoldTransaction.query.all()
        silver_transactions = SilverTransaction.query.all()

        transactions = [{'id': t.id, 'type': 'Gold', 'weight': t.weight, 'price_per_gram': t.price_per_gram,
                         'purity': t.purity, 'service_charge': t.service_charge, 'tax': t.tax, 'total': t.total, 'timestamp': t.timestamp} for t in gold_transactions]

        transactions += [{'id': t.id, 'type': 'Silver', 'weight': t.weight, 'price_per_gram': t.price_per_gram,
                          'purity': t.purity, 'service_charge': t.service_charge, 'tax': t.tax, 'total': t.total, 'timestamp': t.timestamp} for t in silver_transactions]

    return render_template('history.html', transactions=transactions, selected_type=selected_type)


@app.route('/download_csv', methods=['POST'])
def download_csv():
    selected_type = request.args.get('type', 'all')

    si = StringIO()
    writer = csv.writer(si)

    header = ['ID', 'Type', 'Weight (g)', 'Price per Gram', 'Purity', 'Service Charge', 'Tax', 'Total', 'Timestamp']
    writer.writerow(header)

    transactions = []

    if selected_type == 'gold':
        transactions = GoldTransaction.query.all()
        for t in transactions:
            writer.writerow([t.id, 'Gold', t.weight, t.price_per_gram, 'N/A', t.service_charge, t.tax, t.total, t.timestamp])
    elif selected_type == 'silver':
        transactions = SilverTransaction.query.all()
        for t in transactions:
            writer.writerow([t.id, 'Silver', t.weight, t.price_per_gram, t.purity, t.service_charge, t.tax, t.total, t.timestamp])
    else:
        gold_transactions = GoldTransaction.query.all()
        for t in gold_transactions:
            writer.writerow([t.id, 'Gold', t.weight, t.price_per_gram, 'N/A', t.service_charge, t.tax, t.total, t.timestamp])
        silver_transactions = SilverTransaction.query.all()
        for t in silver_transactions:
            writer.writerow([t.id, 'Silver', t.weight, t.price_per_gram, t.purity, t.service_charge, t.tax, t.total, t.timestamp])

    output = si.getvalue().encode('utf-8')
    return send_file(
        BytesIO(output),
        mimetype='text/csv',
        as_attachment=True,
        attachment_filename='transactions.csv'
    )

# Additional routes
@app.route('/pricing')
def pricing() -> str:
    return render_template('pricing.html', config=app.config)

@app.route('/features')
def features() -> str:
    return render_template('features.html', config=app.config)

@app.route('/about')
def about() -> str:
    return render_template('about.html', config=app.config)

if __name__ == '__main__':
    app.run(debug=True)
