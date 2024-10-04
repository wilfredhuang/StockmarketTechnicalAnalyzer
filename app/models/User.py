from ..config.db import db 
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def is_active(self):
        return True  # Return the user's active status


    def is_authenticated(self):
        return True  # Always return True for authenticated users


    def is_anonymous(self):
        return False  # Always return False for authenticated users

    def get_id(self):
        return str(self.id)  # Return the user's ID as a string
    