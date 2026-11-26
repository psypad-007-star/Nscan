
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from app.config import Config
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    # Import models so SQLAlchemy knows about them.
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register routes.
    from app.routes import auth_bp

    app.register_blueprint(auth_bp)

    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database tables initialized.")

    @app.cli.command("reset-db")
    def reset_db():
        db.drop_all()
        db.create_all()
        print("Database reset.")

    @app.route("/health")
    def health():
        return {"status": "healthy"}, 200

    return app
