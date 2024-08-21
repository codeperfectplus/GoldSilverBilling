from src.config import app
from src.models import initialize_database

from src.blueprints import (
    additional_bp,
    admin_bp,
    auth_bp,
    gold_calculator_bp,
    health_bp,
    homepage_bp,
    silver_calculator_bp,
    users_bp
)

# it is used to initialize the database and settings only once when the app starts
@app.before_request
def run_once():
    if not app.config['INITIALIZED']:
        initialize_database()
        app.config['INITIALIZED'] = True

app.register_blueprint(additional_bp)
app.register_blueprint(admin_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(gold_calculator_bp)
app.register_blueprint(health_bp)
app.register_blueprint(homepage_bp)
app.register_blueprint(silver_calculator_bp)
app.register_blueprint(users_bp)



if __name__ == '__main__':
    app.run(debug=True)
