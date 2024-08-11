from flask import Flask, render_template, request
from script import GoldPriceItem  # Import the class from where it's defined

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            price_per_gram = float(request.form['price_per_gram'])
            service_charge = float(request.form['service_charge'])
            tax = float(request.form['tax'])

            # Create an instance of GoldPriceItem
            gold_item = GoldPriceItem(weight, price_per_gram, service_charge, tax)
            bill_details = gold_item.calculate_price()
            return render_template('bill.html', bill=bill_details, weight=weight, price_per_gram=price_per_gram)
        
        except ValueError as e:
            return f"Input error: {str(e)}"
    return render_template('homepage.html')


# pricing
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# features
@app.route('/features')
def features():
    return render_template('features.html')

# about
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
