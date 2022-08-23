from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True,  nullable=False)
    password = db.Column(db.String(60),  nullable=False)
    first_name = db.Column(db.String(20),  nullable=False)
    last_name = db.Column(db.String(20),  nullable=False)


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True,  nullable=False)
    password = db.Column(db.String(60),  nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20),  nullable=False)
    bookings = db.relationship("Booking", backref="booking", lazy=True)


class Flight(db.Model):
    flight_number = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    destination = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    plane_id = db.Column(db.Integer, db.ForeignKey('airplane.plane_id'), nullable=False)
    airport_code_destination = db.Column(db.Integer, db.ForeignKey('airport.airport_code'), nullable=False)
    airport_code_source = db.Column(db.Integer, db.ForeignKey('airport.airport_code'), nullable=False)
    bookings = db.relationship('Booking', backref='flight', lazy=True)


class Airport(db.Model):
    airport_code = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(3), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(3), unique=True, nullable=False)
    departure_flights = db.relationship('Flight', backref='departure_airport', lazy=True, foreign_keys=[Flight.airport_code_source])
    arrival_flights = db.relationship('Flight', backref='arrival_airport', lazy=True, foreign_keys=[Flight.airport_code_destination])


class Airplane(db.Model):
    plane_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(20), unique=True, nullable=False)
    airline_id = db.Column(db.Integer, db.ForeignKey('airline.airline_id'), nullable=False)
    flights = db.relationship('Flight', backref='airplane', lazy=True)


class Airline(db.Model):
    airline_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    airplanes = db.relationship('Airplane', backref='airline', lazy=True)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_time = db.Column(db.DateTime, nullable=False, default=func.now())
    seats = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    flight_number = db.Column(db.Integer, db.ForeignKey('flight.flight_number'),
                              nullable=False)

    __table_args__ = (
        db.UniqueConstraint('customer_id', 'flight_number'),
    )
