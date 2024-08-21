
import logging 

from flask import render_template, request, session, redirect, url_for, flash, Blueprint
from src.calculators import SilverCalculator

from src.config import db
from src.models import Settings, SilverTransaction, JewellerDetails
from src.blueprints.helper import get_currency_symbol

silver_calculator_bp = Blueprint('silver_calculator', __name__)

@silver_calculator_bp.route('/silver-calculator', methods=['GET', 'POST'])
def silver_calculator():
    system_settings = Settings.query.first()
    jeweller_details = JewellerDetails.query.first()
    if not system_settings.is_silver_calculator_enabled:
        return redirect(url_for('permission_denied'))
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

            if silver_price_per_gram <= 0:
                flash('Invalid price per gram. Please enter a valid price.', 'danger')
                return redirect(url_for('silver_calculator.silver_calculator'))
            
            if weight <= 0:
                flash('Invalid weight. Please enter a valid weight.', 'danger')
                return redirect(url_for('silver_calculator.silver_calculator'))
            
            if silver_purity <= 0:
                flash('Invalid purity. Please enter a valid purity.', 'danger')
                return redirect(url_for('silver_calculator.silver_calculator'))

            # Calculate silver price
            silver_item = SilverCalculator(
                weight=weight,
                price_per_gram=silver_price_per_gram,
                service_charge=silver_service_charge,
                tax=silver_tax,
                purity=silver_purity,
            )
            bill_details = silver_item.calculate_price()

            # Save to database
            transaction = SilverTransaction(
                weight=weight,
                price_per_gram=silver_price_per_gram,
                service_charge=silver_service_charge,
                tax=silver_tax,
                total=bill_details['Final Price'],
                currency=system_settings.currency,
                purity=silver_purity
            )
            db.session.add(transaction)
            db.session.commit()
            flash("Bill generated successfully!", 'success')
            flash("Please consider giving a star on GitHub if you find this project useful!", 'info')
                
            return render_template('silver_bill.html',
                                   bill=bill_details,
                                   weight=weight,
                                   price_per_gram=silver_price_per_gram,
                                   purity=silver_purity,
                                   settings=system_settings,
                                   jeweller_details=jeweller_details,
                                   currency_symbol=get_currency_symbol(system_settings.currency))
        except ValueError as e:
            logging.error(f"ValueError in silver calculator: {str(e)}")
            flash(f"Input error: {str(e)}", 'danger')
            return redirect(url_for('silver_calculator.silver_calculator'))

    # Use session-stored price per gram or a default value
    silver_price_per_gram = session.get('silver_price_per_gram', 0)
    silver_service_charge = session.get('silver_service_charge', 0)
    silver_tax = session.get('silver_tax', 0)

    return render_template('silver_calculator.html',
                           price_per_gram=silver_price_per_gram,
                           service_charge=silver_service_charge,
                           tax=silver_tax,
                           settings=system_settings,
                           jeweller_details=jeweller_details,
                           currency_symbol=get_currency_symbol(system_settings.currency))

