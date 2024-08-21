from src.config import app


from src.blueprints.additional import additional_bp
from src.blueprints.admin import admin_bp
from src.blueprints.auth import auth_bp
from src.blueprints.config import config_bp
from src.blueprints.gold_calculator import gold_calculator_bp
from src.blueprints.health import health_bp
from src.blueprints.history import history_bp
from src.blueprints.homepage import homepage_bp
from src.blueprints.silver_calculator import silver_calculator_bp

app.register_blueprint(additional_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(config_bp)
app.register_blueprint(gold_calculator_bp)
app.register_blueprint(health_bp)
app.register_blueprint(history_bp)
app.register_blueprint(homepage_bp)
app.register_blueprint(silver_calculator_bp)



if __name__ == '__main__':
    app.run(debug=True)
