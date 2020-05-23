from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import DebugConfig


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app(config_class=DebugConfig):
    app = Flask('bitey')
    app.config.from_object(config_class)

    from .main.views import main
    from .users.views import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'You have to log in to access this page.'
    login_manager.login_message_category = 'info'

    return app
