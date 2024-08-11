import json
from flask import Flask, render_template, request, session
from flask_session import Session
from src.calcualtors import GoldCalculator, SilverCalculator

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Load configuration from JSON file
def load_config():
    with open('src/config/config.json') as config_file:
        return json.load(config_file)

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

            # Create an instance of GoldPriceItem
            gold_item = GoldCalculator(weight, gold_price_per_gram, service_charge, tax)
            bill_details = gold_item.calculate_price()
            return render_template('gold_bill.html', bill=bill_details, weight=weight, price_per_gram=session.get('gold_price_per_gram', gold_price_per_gram), config=app.config)
        
        except ValueError as e:
            return f"Input error: {str(e)}"
    
    # Retrieve price per gram from session or use a default value
    gold_price_per_gram = session.get('gold_price_per_gram', 6445)
    return render_template('gold_calcualtor.html', price_per_gram=gold_price_per_gram, config=app.config)

@app.route('/silver-calculator', methods=['GET', 'POST'])
def silver_calculator():
    result = None
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            silver_price_per_gram = float(request.form['price_per_gram'])
            purity = float(request.form['purity'])
            service_charge = float(request.form['service_charge'])
            tax = float(request.form['tax'])

            # Save price per gram to session
            session['silver_price_per_gram'] = silver_price_per_gram
            
            silver_item = SilverCalculator(
                weight=weight,
                price_per_gram=silver_price_per_gram,
                service_charge=service_charge,
                tax=tax,
                purity=purity
            )
            result = silver_item.calculate_price()
            return render_template('silver_bill.html', bill=result, weight=weight, price_per_gram=session.get('silver_price_per_gram', silver_price_per_gram), purity=purity, config=app.config)

        except ValueError as e:
            # Handle errors, e.g., show an error message
            print(f"Error: {e}")

    price_per_gram = session.get('silver_price_per_gram', 0)
    return render_template('silver_calculator.html', price_per_gram=price_per_gram, config=app.config)

# Pricing page
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# Features page
@app.route('/features')
def features():
    return render_template('features.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# other calcuators
@app.route('/other-calculators')
def other_calculators():
    return render_template('other_calculators.html')

if __name__ == '__main__':
    app.run(debug=True)
