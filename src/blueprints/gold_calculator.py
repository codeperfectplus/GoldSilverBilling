
import logging 

from flask import render_template, request, session, redirect, url_for, flash, Blueprint
from flask_login import current_user, login_required, login_remembered
from src.calculators import GoldCalculator

from src.config import db
from src.models import Settings, GoldTransaction, JewellerDetails, log_action
from src.blueprints.helper import get_currency_symbol
from src.blueprints.decorators import require_password_change

gold_calculator_bp = Blueprint('gold_calculator', __name__)

# Gold calculator route
@gold_calculator_bp.route('/gold-calculator', methods=['GET', 'POST'])
def gold_calculator():
    system_settings = Settings.query.first()
    jeweller_details = JewellerDetails.query.first()

    if not system_settings.is_gold_calculator_enabled:
        return redirect(url_for('additional.permission_denied'))
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

            if gold_price_per_gram <= 0:
                flash('Invalid gold price per gram.', 'danger')
                return redirect(url_for('gold_calculator.gold_calculator'))

            if weight <= 0:
                flash('Invalid weight.', 'danger')
                return redirect(url_for('gold_calculator.gold_calculator'))

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
                total=bill_details['Final Price'],
                currency=system_settings.currency,
            )
            db.session.add(transaction)
            db.session.commit()

            # if user is logged in, log the transaction
            if current_user.is_authenticated:
                log_action(user_id=current_user.id, username=current_user.username,
                           action='Gold Calculator', details=f"Calculated gold price for weight {weight} grams")
            else:
                log_action(user_id="-1", username="Anonymous",
                           action='Gold Calculator', details=f"Calculated gold price for weight {weight} grams")
                
            flash("Bill generated successfully!", 'success')
            flash("Please consider giving a star on GitHub if you find this project useful!", 'info')
                
            return render_template('calculators/gold_bill.html',
                                   bill=bill_details,
                                   weight=weight,
                                   price_per_gram=gold_price_per_gram,
                                   purity=purity,
                                   settings=system_settings,
                                   jeweller_details=jeweller_details,
                                   currency_symbol=get_currency_symbol(system_settings.currency))
        
        except ValueError as e:
            flash(f"Please enter valid numbers for weight, price per gram, service charge, and tax.", 'danger')
            logging.error(f"ValueError in gold calculator: {str(e)}")
            return redirect(url_for('gold_calculator.gold_calculator'))

    # Use session-stored price per gram or a default value
    gold_price_per_gram = session.get('gold_price_per_gram', 0)
    gold_service_charge = session.get('gold_service_charge', 0)
    gold_tax = session.get('gold_tax', 0)

    return render_template('calculators/gold_calculator.html',
                           price_per_gram=gold_price_per_gram,
                           service_charge=gold_service_charge,
                           tax=gold_tax,
                           settings=system_settings,
                           jeweller_details=jeweller_details,
                           currency_symbol=get_currency_symbol(system_settings.currency))
                           

