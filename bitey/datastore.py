from flask_security import SQLAlchemyUserDatastore
from bitey import db
from bitey.users.models import User, Role


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
