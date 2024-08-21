import psutil
import csv
from io import StringIO, BytesIO

from flask import render_template, request, session, redirect, url_for, flash, Blueprint
from flask import request, send_file, Blueprint
from flask_login import current_user, login_required

from src.config import db
from src.models import User, AuditLog, Settings, log_action
from src.models import GoldTransaction, SilverTransaction, JewellerDetails, Settings

admin_bp = Blueprint('admin_', __name__)


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if current_user.user_level != 'admin':
        return redirect(url_for('home'))
    
    # Convert string 'true'/'false' to boolean True/False
    logs = []

    def str_to_bool(value):
        return value.lower() == 'true'

    if request.method == 'POST':
        currency = request.form.get('currency', 'INR')
        theme = request.form.get('theme', 'light')
        language = request.form.get('language', 'en')
        flash_message_timeout = int(request.form.get('flash_message_timeout', 5))
        is_flash_message_enabled = str_to_bool(request.form.get('is_flash_message_enabled', 'true'))
        is_gold_jewellers_sidebar = str_to_bool(request.form.get('is_gold_jewellers_sidebar', 'true'))
        is_gold_calculator_enabled = str_to_bool(request.form.get('is_gold_calculator_enabled', 'true'))
        is_silver_calculator_enabled = str_to_bool(request.form.get('is_silver_calculator_enabled', 'true'))
        
        settings = Settings.query.first()
        if settings.is_gold_jewellers_sidebar != is_gold_jewellers_sidebar:
            # log_action(current_user.id, current_user.username, 'System Settings Change', details=f"Sidebar Status Changed from {settings.is_gold_jewellers_sidebar} to {is_gold_jewellers_sidebar}")
            logs.append(f"Sidebar Status Changed from {settings.is_gold_jewellers_sidebar} to {is_gold_jewellers_sidebar}")
            settings.is_gold_jewellers_sidebar = is_gold_jewellers_sidebar

        if settings.is_gold_calculator_enabled != is_gold_calculator_enabled:
            logs.append(f"Gold Calculator Status Changed from {settings.is_gold_calculator_enabled} to {is_gold_calculator_enabled}")
            settings.is_gold_calculator_enabled = is_gold_calculator_enabled

        if settings.is_silver_calculator_enabled != is_silver_calculator_enabled:
            logs.append(f"Silver Calculator Status Changed from {settings.is_silver_calculator_enabled} to {is_silver_calculator_enabled}")
            settings.is_silver_calculator_enabled = is_silver_calculator_enabled

        if settings.is_flash_message_enabled != is_flash_message_enabled:
            logs.append(f"Flash Message Status Changed from {settings.is_flash_message_enabled} to {is_flash_message_enabled}")
            settings.is_flash_message_enabled = is_flash_message_enabled

        if settings.flash_message_timeout != flash_message_timeout:
            logs.append(f"Flash Message Timeout Changed from {settings.flash_message_timeout} to {flash_message_timeout}")
            settings.flash_message_timeout = flash_message_timeout        

        if settings.currency != currency:
            logs.append(f"Currency Changed from {settings.currency} to {currency}")
            settings.currency = currency

        if settings.theme != theme:
            logs.append(f"Theme Changed from {settings.theme} to {theme}")
            settings.theme = theme

        if settings.language != language:
            logs.append(f"Language Changed from {settings.language} to {language}")
            settings.language = language

        # if not settings changes add no changed done message, and dont't commit
        if not logs:
            flash("No changes made.", 'info')
            return redirect(url_for('admin_.settings'))

        log_action(current_user.id, current_user.username, 'System Settings Change', details=logs)
        
        if not settings:
            settings = Settings(currency=currency, theme=theme, language=language,
                                is_flash_message_enabled=is_flash_message_enabled,
                                flash_message_timeout=flash_message_timeout,
                                is_gold_jewellers_sidebar=is_gold_jewellers_sidebar,
                                is_gold_calculator_enabled=is_gold_calculator_enabled,
                                is_silver_calculator_enabled=is_silver_calculator_enabled)
            
        else:
            settings.currency = currency
            settings.theme = theme
            settings.language = language
            settings.is_flash_message_enabled = is_flash_message_enabled 
            settings.flash_message_timeout = flash_message_timeout
            settings.is_gold_jewellers_sidebar = is_gold_jewellers_sidebar
            settings.is_gold_calculator_enabled = is_gold_calculator_enabled
            settings.is_silver_calculator_enabled = is_silver_calculator_enabled

        db.session.add(settings)
        db.session.commit()
        for log in logs:
            flash(log, 'success')
        return redirect(url_for('admin_.settings'))
    
    settings = Settings.query.first()
    return render_template('dashboard/settings.html', settings=settings)


@admin_bp.route('/audit_log')
@login_required
def audit_log():
    if current_user.user_level != 'admin':
        return redirect(url_for('home'))

    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template('dashboard/audit_log.html', logs=logs)


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    system_settings = Settings.query.first()
    audit_logs = AuditLog.query.filter_by(user_id=current_user.id).order_by(AuditLog.timestamp.desc()).all()
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
        elif cpu_utilization > 60:
            system_health = "Moderate"
        elif cpu_utilization > 40:
            system_health = "Fair"
        elif cpu_utilization > 20:
            system_health = "Good"
        else:
            system_health = "Excellent"

        return render_template('dashboard/admin_dashboard.html', 
                            total_users=total_users, 
                            active_sessions=active_sessions, 
                            system_health=system_health,
                            cpu_core=cpu_core,
                            cpu_util=cpu_utilization,
                            audit_logs=audit_logs,
                            settings=system_settings,
                            current_user=current_user)
    
    elif current_user.user_level == 'customer':
        audit_logs = AuditLog.query.filter_by(user_id=current_user.id)
        return render_template('dashboard/customer_dashboard.html', settings=system_settings)
 
# Silver calculator route
@admin_bp.route('/history', methods=['GET'])
@login_required
def history():
    if current_user.user_level != 'admin':
        return redirect(url_for('additional.permission_denied'))
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

    return render_template('dashboard/history.html', transactions=transactions, selected_type=selected_type)

@admin_bp.route('/download_audit_log', methods=['POST'])
def download_audit_log():
    logs = AuditLog.query.all()
    si = StringIO()
    writer = csv.writer(si)

    header = ['ID', 'User ID', 'Action', 'description', 'Timestamp']
    writer.writerow(header)

    for log in logs:
        writer.writerow([log.id, log.user_id, log.action, log.details, log.timestamp])

    output = si.getvalue().encode('utf-8')
    return send_file(BytesIO(output), as_attachment=True, download_name='audit_log.csv')

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
    system_settings = Settings.query.first()
    if current_user.user_level != 'admin':
        return redirect(url_for('additional.permission_denied'))
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
        return redirect(url_for('admin_.update_jeweller_details'))

    jeweller = JewellerDetails.query.first()
    return render_template('dashboard/config.html', jeweller=jeweller, settings=system_settings)
