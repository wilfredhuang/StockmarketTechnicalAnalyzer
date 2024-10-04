from ..config.db import db 
from flask_login import UserMixin

class StockTicker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shares = db.Column(db.Integer, nullable=False)  # New column for number of shares
    price = db.Column(db.Float, nullable=False)  # New column for price per share