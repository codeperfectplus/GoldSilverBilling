import csv
from io import StringIO, BytesIO

from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import current_user, login_required

from flask import request, send_file, Blueprint

from src.models import GoldTransaction, SilverTransaction

history_bp = Blueprint('history', __name__)

# Silver calculator route
@history_bp.route('/history', methods=['GET'])
@login_required
def history():
    if current_user.user_level != 'admin':
        return redirect(url_for('permission_denied'))
    selected_type = request.args.get('type', 'all')

    if selected_type == 'gold':
        transactions = GoldTransaction.query.all()
        transactions = [{'id': t.id, 'type': 'Gold', 'weight': t.weight, 'price_per_gram': t.price_per_gram, 
                         "purity": t.purity, 'service_charge': t.service_charge, 'tax': t.tax, 'total': t.total, 'currency': t.currency,
                         'timestamp': t.timestamp} for t in transactions]
    elif selected_type == 'silver':
        transactions = SilverTransaction.query.all()
        transactions = [{'id': t.id, 'type': 'Silver', 'weight': t.weight, 'price_per_gram': t.price_per_gram,
                         'purity': t.purity, 'service_charge': t.service_charge, 'tax': t.tax, 'total': t.total, 'currency': t.currency,
                         'timestamp': t.timestamp} for t in transactions]
    else:
        gold_transactions = GoldTransaction.query.all()
        silver_transactions = SilverTransaction.query.all()

        transactions = [{'id': t.id, 'type': 'Gold', 'weight': t.weight, 'price_per_gram': t.price_per_gram,
                         'purity': t.purity, 'service_charge': t.service_charge, 'tax': t.tax, 'total': t.total, 'currency': t.currency,
                         'timestamp': t.timestamp} for t in gold_transactions]

        transactions += [{'id': t.id, 'type': 'Silver', 'weight': t.weight, 'price_per_gram': t.price_per_gram,
                          'purity': t.purity, 'service_charge': t.service_charge, 'tax': t.tax, 'total': t.total, 'currency': t.currency,
                          'timestamp': t.timestamp} for t in silver_transactions]

    return render_template('history.html', transactions=transactions, selected_type=selected_type)

@history_bp.route('/download_transactions_history', methods=['POST'])
def download_transactions_history():
    selected_type = request.args.get('type', 'all')

    si = StringIO()
    writer = csv.writer(si)

    header = ['ID', 'Type', 'Weight (g)', 'Price per Gram', 'Purity', 'Service Charge', 'Tax', 'Total', 'Timestamp']
    writer.writerow(header)

    transactions = []

    if selected_type == 'gold':
        transactions = GoldTransaction.query.all()
        for t in transactions:
            writer.writerow([t.id, 'Gold', t.weight, t.price_per_gram, t.purity, t.service_charge, t.tax, t.total, t.currency,
                             t.timestamp])
    elif selected_type == 'silver':
        transactions = SilverTransaction.query.all()
        for t in transactions:
            writer.writerow([t.id, 'Silver', t.weight, t.price_per_gram, t.purity, t.service_charge, t.tax, t.total, t.currency,
                             t.timestamp])
    else:
        gold_transactions = GoldTransaction.query.all()
        for t in gold_transactions:
            writer.writerow([t.id, 'Gold', t.weight, t.price_per_gram, t.purity, t.service_charge, t.tax, t.total, t.currency,
                             t.timestamp])
        silver_transactions = SilverTransaction.query.all()
        for t in silver_transactions:
            writer.writerow([t.id, 'Silver', t.weight, t.price_per_gram, t.purity, t.service_charge, t.tax, t.total, t.currency,
                             t.timestamp])

    output = si.getvalue().encode('utf-8')
    return send_file(
        BytesIO(output),
        mimetype='text/csv',
        as_attachment=True,
        download_name='transactions.csv'
    )
