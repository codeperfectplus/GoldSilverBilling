import json
from flask import Flask, render_template, request, session
from flask_session import Session
from src.script import GoldPriceItem

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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            price_per_gram = float(request.form['price_per_gram'])
            service_charge = float(request.form['service_charge'])
            tax = float(request.form['tax'])
            
            # Save price per gram to session
            session['price_per_gram'] = price_per_gram

            # Create an instance of GoldPriceItem
            gold_item = GoldPriceItem(weight, price_per_gram, service_charge, tax)
            bill_details = gold_item.calculate_price()
            return render_template('bill.html', bill=bill_details, weight=weight, price_per_gram=session.get('price_per_gram', price_per_gram), config=app.config)
        
        except ValueError as e:
            return f"Input error: {str(e)}"
    
    # Retrieve price per gram from session or use a default value
    price_per_gram = session.get('price_per_gram', 6445)
    return render_template('homepage.html', price_per_gram=price_per_gram, config=app.config)

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

if __name__ == '__main__':
    app.run(debug=True)
