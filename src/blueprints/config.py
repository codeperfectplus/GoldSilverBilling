
from flask import render_template, request, redirect, url_for, Blueprint

from src.config import db
from src.models import JewellerDetails

config_bp = Blueprint('config', __name__)

@config_bp.route('/config', methods=['GET', 'POST'])
def update_jeweller_details():
    if request.method == 'POST':
        jeweller = JewellerDetails.query.first()

        jeweller.jeweller_name = request.form['jeweller_name']
        jeweller.jeweller_address = request.form['jeweller_address']
        jeweller.jeweller_contact = request.form['jeweller_contact']
        jeweller.jeweller_email = request.form['jeweller_email']
        jeweller.jeweller_website = request.form['jeweller_website']
        jeweller.jeweller_gstin = request.form['jeweller_gstin']
        jeweller.gold_price_per_gram = float(request.form['gold_price_per_gram'])

        if 'jeweller_logo' in request.files:
            logo = request.files['jeweller_logo']
            logo.save(f'static/images/{logo.filename}')
            jeweller.jeweller_logo = f'images/{logo.filename}'

        db.session.commit()
        return redirect(url_for('update_jeweller_details'))

    jeweller = JewellerDetails.query.first()
    return render_template('config.html', jeweller=jeweller)


