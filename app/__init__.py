from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensions initialization will go here
    
    # Blueprints registration
    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
