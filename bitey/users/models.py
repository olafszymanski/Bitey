from bitey import login_manager, db
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    activated = db.Column(db.Boolean, default=False)
    activated_on = db.Column(db.DateTime, default=None)
    created_on = db.Column(db.DateTime, default=datetime.now())


    def __init__(self, username, email, password, name=None, last_name=None, address=None, activated=False, activated_on=None, created_on=datetime.now()):
        self.username = username
        self.email = email
        self.password = password
        self.name = name
        self.last_name = last_name
        self.address = address
        self.activated = activated
        self.activated_on = activated_on
        self.created_on = created_on


    def __repr__(self):
        return f'User({self.id}, {self.username})'
