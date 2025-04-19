from .database import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    advisor_id = db.Column(db.Integer, db.ForeignKey('advisor.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='tentative', nullable=False)
    google_event_id = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    appointments = db.relationship('Appointment', backref='user', lazy=True)

class Advisor(db.Model):
    __tablename__ = 'advisor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    google_calendar_id = db.Column(db.String(200))
    google_access_token = db.Column(db.String(500))
    google_refresh_token = db.Column(db.String(500))
    token_expiry = db.Column(db.DateTime)
    appointments = db.relationship('Appointment', backref='advisor', lazy=True)

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    mercadopago_id = db.Column(db.String(100))
    status = db.Column(db.String(20))  # pending, approved, rejected
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    appointment = db.relationship('Appointment', backref='payment', uselist=False) 