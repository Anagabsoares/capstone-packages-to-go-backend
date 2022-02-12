from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")


    from app.models.user import User
    from app.models.package import Package
    from app.models.notification import Notification

    db.init_app(app)
    migrate.init_app(app, db)


    from .routes.packages import packages_bp
    from .routes.users import users_bp
    from .routes.notifications import notifications_bp

    app.register_blueprint(packages_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(notifications_bp)

    CORS(app)


    return app