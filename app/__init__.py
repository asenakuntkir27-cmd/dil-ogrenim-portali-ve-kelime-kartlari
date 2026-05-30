from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Lütfen bu sayfayı görüntülemek için giriş yapın.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensions initialization
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Import models
    from app import models
    
    # Blueprints registration
    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Register CLI commands
    @app.cli.command("seed")
    def seed_command():
        """Seed the database with initial data."""
        from app.seeds import seed_db
        seed_db()

    # Automatic database setup and seeding on startup (if not in testing mode)
    if not app.config.get('TESTING'):
        with app.app_context():
            import sqlalchemy as sa
            from app.models import User
            try:
                # Veritabanının sağlıklı olup olmadığını anlamak için deneme sorgusu çek
                db.session.scalar(sa.select(User.id).limit(1))
                
                # Şema sağlamsa doğrudan tohumlama/eksik kontrolü yap
                from app.seeds import seed_db
                seed_db()
            except Exception as e:
                # Tablolar eksik, bozuk veya eski migrasyonlardan kalma uyumsuzluk var
                db.session.rollback()
                print(f"Database check failed: {e}. Attempting auto-recovery...")
                try:
                    db.drop_all()
                    db.create_all()
                    from app.seeds import seed_db
                    seed_db()
                    print("Database auto-recovered successfully.")
                except Exception as recovery_error:
                    db.session.rollback()
                    print(f"CRITICAL: Failed to auto-recover database: {recovery_error}")

    return app
