from flask import render_template, Blueprint

from src.models import Settings

homepage_bp = Blueprint('homepage', __name__)

@homepage_bp.route('/')
def home() -> str:
    system_settings = Settings.query.first()
    return render_template('homepage.html', is_gold_calculator_enabled=system_settings.is_gold_calculator_enabled,
                           is_silver_calculator_enabled=system_settings.is_silver_calculator_enabled)