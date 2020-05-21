from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from .config import DebugConfig


db = SQLAlchemy()
security = Security()


def create_app(config_class=DebugConfig):
    app = Flask('Bitey')
    app.config.from_object(config_class)

    from .main.views import main

    app.register_blueprint(main)

    db.init_app(app)
    security.init_app(app)

    return app
