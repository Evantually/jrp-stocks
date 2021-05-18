from app import db
from datetime import datetime

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    ticker = db.Column(db.String(5), index=True, unique=True)
    shares_outstanding = db.Column(db.Integer, nullable=False, default=50000)
    share_price = db.Column(db.Float, nullable=False, default=50)
    ipo_price = db.Column(db.Float, nullable=False, default=1)
    equity = db.Column(db.Float, nullable=False, default=50000)
    market_cap = db.Column(db.Float, nullable=False, default=50000)
    price_earnings = db.Column(db.Float, nullable=False, default=1)
    trades = db.relationship('Trade', backref='jrp_company', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shares = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_executed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    company = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self):
        return '{} exchanged {} shares at {}'.format(self.jrp_company, self.shares, self.time)

class MarketOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.Integer, db.ForeignKey('company.id'))
    shares = db.Column(db.Integer, nullable=False)
    share_price = db.Column(db.Float, nullable=False)
    time_placed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)