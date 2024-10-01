from .db import db 
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
    
class StockTicker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shares = db.Column(db.Integer, nullable=False)  # New column for number of shares
    price = db.Column(db.Float, nullable=False)  # New column for price per share