import psutil
import csv
from io import StringIO, BytesIO

from flask import render_template, request, session, redirect, url_for, flash, Blueprint
from flask import request, send_file, Blueprint
from flask_login import current_user, login_required

from src.config import db
from src.models import User, AuditLog, Settings, log_action
from src.models import GoldTransaction, SilverTransaction, JewellerDetails

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.user_level != 'admin':
        return redirect(url_for('permission_denied'))

    users = User.query.all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_level = request.form.get('user_level')
        
        user = User.query.get(user_id)
        if user:
            user.user_level = new_level
            db.session.commit()
            flash(f"User {user.username}'s level updated to {new_level}.", 'success')
        else:
            flash("User not found.", 'error')

    return render_template('manage_users.html', users=users)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if current_user.user_level != 'admin':
        return redirect(url_for('home'))

    if request.method == 'POST':
        currency = request.form.get('currency')
        theme = request.form.get('theme')
        language = request.form.get('language')
        is_gold_jewellers_sidebar = int(request.form.get('is_gold_jewellers_sidebar'))
        is_gold_calculator_enabled = int(request.form.get('is_gold_calculator_enabled'))
        is_silver_calculator_enabled = int(request.form.get('is_silver_calculator_enabled'))

        # Save the settings (you might save them to a database or a config file)
        # Assuming you have a Settings model or similar logic to save settings
        settings = Settings.query.first()
        if not settings:
            settings = Settings(currency=currency, theme=theme, language=language,
                                is_gold_jewellers_sidebar=is_gold_jewellers_sidebar,
                                is_gold_calculator_enabled=is_gold_calculator_enabled,
                                is_silver_calculator_enabled=is_silver_calculator_enabled)
        else:
            settings.currency = currency
            settings.theme = theme
            settings.language = language
            settings.is_gold_jewellers_sidebar = is_gold_jewellers_sidebar
            settings.is_gold_calculator_enabled = is_gold_calculator_enabled
            settings.is_silver_calculator_enabled = is_silver_calculator_enabled

        db.session.add(settings)
        db.session.commit()
        flash('System settings updated successfully!', 'success')
        log_action(current_user.id, current_user.username, 'System Settings Change', details=f"Currency set to {currency}, Theme set to {theme}")
        return redirect(url_for('admin.settings'))
    
    settings = Settings.query.first()
    return render_template('settings.html', settings=settings)


@admin_bp.route('/audit_log')
@login_required
def audit_log():
    if current_user.user_level != 'admin':
        return redirect(url_for('home'))

    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template('audit_log.html', logs=logs)


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.user_level == 'admin':
        total_users = User.query.count()  # Count total users
        active_sessions = len(session)  # This is a basic approach. You may want to track sessions differently.
        
        # Example: If you store active users in the session, you might track like this:
        active_sessions = session.get('active_users', 0)
        
        system_health = "Good"  # This can be determined by your own logic
        cpu_core = psutil.cpu_count()
        cpu_utilization = psutil.cpu_percent(interval=1)

        if cpu_utilization > 80:
            system_health = "Warning"
        else:
            system_health = "Good"

        audit_logs = AuditLog.query.filter_by(user_id=current_user.id).all()
        return render_template('admin_dashboard.html', 
                            total_users=total_users, 
                            active_sessions=active_sessions, 
                            system_health=system_health,
                            cpu_core=cpu_core,
                            cpu_util=cpu_utilization,
                            audit_logs=audit_logs)
    elif current_user.user_level == 'customer':
        audit_logs = AuditLog.query.filter_by(user_id=current_user.id).all()
        return render_template('customer_dashboard.html', audit_logs=audit_logs)
 
# Silver calculator route
@admin_bp.route('/history', methods=['GET'])
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

@admin_bp.route('/download_transactions_history', methods=['POST'])
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


@admin_bp.route('/config', methods=['GET', 'POST'])
@login_required
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

        if 'jeweller_logo' in request.files and request.files['jeweller_logo'].filename:
            logo = request.files['jeweller_logo']
            logo_path = f'src/static/images/{logo.filename}'
            logo.save(logo_path)
            jeweller.jeweller_logo = f'images/{logo.filename}'

        db.session.commit()

        flash('Jeweller details updated successfully!', 'success')
        return redirect(url_for('admin.update_jeweller_details'))

    jeweller = JewellerDetails.query.first()
    return render_template('config.html', jeweller=jeweller)
