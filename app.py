import os
import json
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_session import Session

from src.calcualtors import GoldCalculator, SilverCalculator

app = Flask(__name__)

# Secret key and session configuration
app.secret_key = os.environ.get('SECRET_KEY', 'jhd87^&*^udhwduy792ejlndhy783uh')  # Use environment variable for secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, 'config.json')

# Load configuration from JSON file
def load_config():
    try:
        with open(CONFIG_FILE_PATH) as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file not found at {CONFIG_FILE_PATH}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON config: {e}")
        return {}

app.config.update(load_config())

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/gold-calculator', methods=['GET', 'POST'])
def gold_calculator():
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            gold_price_per_gram = float(request.form['price_per_gram'])
            service_charge = float(request.form['service_charge'])
            tax = float(request.form['tax'])
            
            # Save price per gram to session
            session['gold_price_per_gram'] = gold_price_per_gram

            # Calculate gold price
            gold_item = GoldCalculator(weight, gold_price_per_gram, service_charge, tax)
            bill_details = gold_item.calculate_price()
            
            return render_template('gold_bill.html', 
                                   bill=bill_details, 
                                   weight=weight, 
                                   price_per_gram=gold_price_per_gram, 
                                   config=app.config)
        except ValueError as e:
            flash(f"Input error: {str(e)}", 'error')
            return redirect(url_for('gold_calculator'))
    
    # Use session-stored price per gram or a default value
    gold_price_per_gram = session.get('gold_price_per_gram', 6445)
    return render_template('gold_calculator.html', 
                           price_per_gram=gold_price_per_gram, 
                           config=app.config)

@app.route('/silver-calculator', methods=['GET', 'POST'])
def silver_calculator():
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            silver_price_per_gram = float(request.form['price_per_gram'])
            purity = float(request.form['purity'])
            service_charge = float(request.form['service_charge'])
            tax = float(request.form['tax'])

            # Save price per gram to session
            session['silver_price_per_gram'] = silver_price_per_gram
            
            # Calculate silver price
            silver_item = SilverCalculator(
                weight=weight,
                price_per_gram=silver_price_per_gram,
                service_charge=service_charge,
                tax=tax,
                purity=purity
            )
            bill_details = silver_item.calculate_price()
            
            return render_template('silver_bill.html', 
                                   bill=bill_details, 
                                   weight=weight, 
                                   price_per_gram=silver_price_per_gram, 
                                   purity=purity, 
                                   config=app.config)
        except ValueError as e:
            flash(f"Input error: {str(e)}", 'error')
            return redirect(url_for('silver_calculator'))

    # Use session-stored price per gram or a default value
    silver_price_per_gram = session.get('silver_price_per_gram', 0)
    return render_template('silver_calculator.html', 
                           price_per_gram=silver_price_per_gram, 
                           config=app.config)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', config=app.config)

@app.route('/features')
def features():
    return render_template('features.html', config=app.config)

@app.route('/about')
def about():
    return render_template('about.html', config=app.config)

@app.route('/other-calculators')
def other_calculators():
    return render_template('other_calculators.html', config=app.config)

if __name__ == '__main__':
    app.run()
