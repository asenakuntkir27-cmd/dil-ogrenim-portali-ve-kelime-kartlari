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
    
    from flask_talisman import Talisman
    # Geliştirme/yerel ağ testlerinde (0.0.0.0:5000) mobil cihazların HTTPS yönlendirme hatası
    # almaması için force_https=False olarak yapılandırılmıştır.
    Talisman(app, content_security_policy=None, force_https=False)
    
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
            from sqlalchemy import inspect
            try:
                # Veritabanında olması gereken ve mevcut tabloları doğrula
                inspector = inspect(db.engine)
                existing_tables = inspector.get_table_names()
                expected_tables = list(db.metadata.tables.keys())
                
                missing_tables = [table for table in expected_tables if table not in existing_tables]
                if missing_tables:
                    raise Exception(f"Eksik tablolar tespit edildi: {missing_tables}")
                
                # Tablolar mevcutsa temel bir sorgu çekmeyi dene (bütünlük testi)
                import sqlalchemy as sa
                from app.models import User, Deck
                db.session.scalar(sa.select(User.id).limit(1))
                db.session.scalars(sa.select(Deck).limit(1)).first()
                
                # Şema sağlamsa doğrudan tohumlama/eksik kontrolü yap
                from app.seeds import seed_db
                success = seed_db()
                if not success:
                    raise Exception("Veritabanı tohumlama başarısız oldu, şema uyuşmazlığı olabilir.")
            except Exception as e:
                # Tablolar eksik, bozuk veya eski migrasyonlardan kalma uyumsuzluk var
                db.session.remove()  # Scoped session'ı tamamen kaldır
                print(f"Database verification failed: {e}. Attempting clean auto-recovery...")
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
