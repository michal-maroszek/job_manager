from dotenv import load_dotenv
from os import path
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

# REMEMBER: Add imports in alphabetical order !!!

load_dotenv()

# Initialazing a DB
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"sqlite:///{DB_NAME}"  # telling Flask where the database is located
    db.init_app(app)  # telling the database that this is the app we are going to use

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Client, Job  # loading models before creating database

    with app.app_context():
        # FIXME: In a production application, you would also need to deal
        #  with the need for making changes to your models as new features are
        #  added to the app. Therefore, you would need to use something like:
        #  https://pypi.org/project/alembic/
        #  (Consider what would happen if you wanted to change the "info"
        #  field to "information" in an app already being used,
        #  with multiple users, clients, and jobs.)
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # where should flask redirect when user is NOT logged in and login is REQUIRED
    login_manager.init_app(app)  # telling login manager what app we use

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(
            int(id)
        )  # telling flask how we load a user, by default query.get() look for PRIMARY KEY

    return app
