from bitey import login_manager, db
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())


    def __init__(self, name, last_name, username, email, password, active=False, created_at=datetime.now()):
        self.name = name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.active = active
        self.created_at = created_at


    def __repr__(self):
        return f'User({self.id}, {self.username})'
