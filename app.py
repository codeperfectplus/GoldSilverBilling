import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_session import Session
from calcualtors import GoldCalculator, SilverCalculator

# Initialize the Flask app
app = Flask(__name__)

# Load configuration from environment variables or fallback to defaults
app.secret_key = os.getenv('SECRET_KEY', 'jhd87^&*^udhwduy792ejlndhy783uh')  # Strongly recommended to set this via env vars
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
