import json

from flask import Blueprint, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
from sqlalchemy import cast, Date, and_
from sqlalchemy.orm import aliased
from werkzeug.utils import redirect

from .forms import *
from .models import *
from . import mysql

views = Blueprint('views', __name__)


@views.route('/')
def index():
    if current_user.is_authenticated and session['account_type'] == 'customer':
        return render_template("customer/index.html", user=current_user)
    elif current_user.is_authenticated and session['account_type'] == 'staff':
        return render_template("staff/index.html", user=current_user)
    # cur = mysql.connection.cursor()
    # result = cur.execute("SELECT * FROM flight")
    # if result > 0:
    #     values = cur.fetchall()
    #     print(values)
    # cur.close()
    return render_template("index.html", user=current_user)


@views.route("/customer/search_flight", methods=['GET', 'POST'])
@login_required
def search_flight():
    form = SearchFlightForm()
    airports = db.session.query(Airport).all()
    form.dest_city.choices = [(i.city, i.city) for i in airports]
    form.source_city.choices = [(i.city, i.city) for i in airports]
    # form.dest_airport.choices = [(i.name, i.name) for i in airports]
    # form.source_airport.choices = [(i.name, i.name) for i in airports]
    if form.validate_on_submit():
        source_city = form.source_city.data
        destin_city = form.dest_city.data
        flight_date = form.flight_date.data
        a1 = aliased(Airport)
        a2 = aliased(Airport)
        f = aliased(Flight)
        data = db.session.query(f.flight_number,
                                f.start_time,
                                f.end_time,
                                f.source,
                                f.destination,
                                f.status,
                                a1.name.label("source_airport"),
                                a2.name.label("destination_airport")) \
            .join(a1, a1.airport_code == f.airport_code_source) \
            .join(a2, a2.airport_code == f.airport_code_destination) \
            .filter(f.source == source_city,
                    f.destination == destin_city,
                    cast(f.start_time, Date) == flight_date
                    ).all()
        if data:
            return render_template("customer/flight_result.html", user=current_user, data=data)
        else:
            flash("No flights on this day", "error")

    return render_template("customer/search_flight.html", user=current_user, form=form)


@views.route("/customer/book_flight", methods=['GET', 'POST'])
@login_required
def book_flight():
    form = BookFlightForm()
    flights = db.session.query(Flight).all()
    form.flight_number.choices = [(i.flight_number, i.flight_number) for i in flights]

    if form.validate_on_submit():
        flight_number = form.flight_number.data
        seats = form.seats.data
        flight = db.session.query(Flight).filter_by(flight_number=flight_number).first()
        booking = db.session.query(Booking).filter(
            and_(Booking.flight_number == flight_number, Booking.customer_id == current_user.id)).first()
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM booking WHERE flight_number=%s", (flight_number,))
        num_bookings = cur.fetchone()[0]
        cur.close()
        if booking is not None:
            flash('You already booked this flight', "error")
        elif seats > flight.capacity:
            flash('There is no space in this flight', "error")
        # elif len(flight.bookings) >= flight.capacity:
        elif num_bookings >= flight.capacity:
            flash('This is flight is full', "error")
        else:
            new_booking = Booking(flight_number=flight_number,
                                  seats=seats,
                                  customer_id=current_user.id)
            db.session.add(new_booking)
            db.session.commit()
            flash('You have booked flight with number' + str(new_booking.id))
            return redirect(url_for('views.index'))

    return render_template("customer/book_flight.html", user=current_user, form=form)


@views.route("/customer/my_bookings")
@login_required
def my_bookings():
    a1 = aliased(Airport)
    a2 = aliased(Airport)
    f = aliased(Flight)
    data = db.session.query(Booking,
                            f,
                            a1.name.label("source_airport"),
                            a2.name.label("destination_airport")).join(f, Booking.flight_number == f.flight_number) \
        .join(a1, a1.airport_code == f.airport_code_source) \
        .join(a2, a2.airport_code == f.airport_code_destination) \
        .filter(Booking.customer_id == current_user.id).all()
    if data:
        return render_template("customer/my_bookings.html", user=current_user, data=data)
    else:
        flash("You don't have any bookings", "error")
        return redirect(url_for('views.index'))


@views.route('/delete-booking', methods=['POST'])
def delete_booking():
    booking = json.loads(request.data)
    booking_id = booking['bookingId']
    booking = db.session.query(Booking).filter_by(id=booking_id).first()
    if booking:
        if booking.customer_id == current_user.id:
            db.session.delete(booking)
            db.session.commit()

    return jsonify({})


@views.route("/staff/add_airplane", methods=['GET', 'POST'])
@login_required
def add_airplane():
    if not session["account_type"] == 'staff':
        flash('You must be logged in as an airline staff for this action', "error")
        return redirect(url_for('views.index'))
    form = AddAirplaneForm()
    airlines = db.session.query(Airline).all()
    form.airline_name.choices = [(i.airline_id, i.name) for i in airlines]
    if form.validate_on_submit():
        model = form.model.data
        airline_id = form.airline_name.data
        airplane = db.session.query(Airplane).filter_by(model=model).first()
        if not airplane:
            new_plane = Airplane(model=model, airline_id=airline_id)
            db.session.add(new_plane)
            db.session.commit()
            flash(f'You have added airplane {model} to the system')
            return redirect(url_for('views.index'))
        else:
            flash('There is already an airplane with this model', "error")

    return render_template("staff/add_airplane.html", user=current_user, form=form)


@views.route("/staff/add_airport", methods=['GET', 'POST'])
@login_required
def add_airport():
    if not session["account_type"] == 'staff':
        flash('You must be logged in as an airline staff for this action', "error")
        return redirect(url_for('views.index'))
    form = AddAirportForm()
    if form.validate_on_submit():
        name = form.name.data
        airport = db.session.query(Airport).filter_by(name=name).first()
        if airport is None:
            new_airport = Airport(country=form.country.data,
                                  city=form.city.data,
                                  name=form.name.data)
            db.session.add(new_airport)
            db.session.commit()
            flash(f'You have added airport {name} to the system')
            return redirect(url_for('views.index'))
        else:
            flash('There is already an airport with this name', "error")

    return render_template("staff/add_airport.html", user=current_user, form=form)


@views.route("/staff/add_flight", methods=['GET', 'POST'])
@login_required
def add_flight():
    if not session["account_type"] == 'staff':
        flash('You must be logged in as an airline staff for this action', "error")
        return redirect(url_for('views.index'))
    form = AddFlightForm()
    airports = db.session.query(Airport).all()
    airplanes = db.session.query(Airplane).all()
    form.source.choices = [(i.city, i.city) for i in airports]
    form.destination.choices = [(i.city, i.city) for i in airports]
    form.airport_destination.choices = [(i.airport_code, i.name) for i in airports]
    form.airport_source.choices = [(i.airport_code, i.name) for i in airports]

    form.airplane.choices = [(i.plane_id, i.model) for i in airplanes]
    if form.validate_on_submit():
        start_time = form.start_time.data
        end_time = form.end_time.data
        destination = form.destination.data
        source = form.source.data
        capacity = form.capacity.data
        status = form.status.data
        plane_id = form.airplane.data
        airport_code_destination = form.airport_destination.data
        airport_code_source = form.airport_source.data
        # flight = db.session.query(Flight).filter_by(start_time=start_time, plane_id=plane_id).first()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM flight WHERE start_time=%s AND plane_id=%s", (start_time, plane_id))
        flight = cur.fetchone()
        cur.close()
        if not flight:
            new_flight = Flight(start_time=start_time,
                                end_time=end_time,
                                destination=destination,
                                source=source,
                                capacity=capacity,
                                status=status,
                                plane_id=plane_id,
                                airport_code_destination=airport_code_destination,
                                airport_code_source=airport_code_source
                                )
            db.session.add(new_flight)
            db.session.commit()
            flash(f'You have added flight {new_flight.flight_number} to the system')
            return redirect(url_for('views.index'))
        else:
            flash('There is already a flight of this airplane on this time', "error")

    return render_template("staff/add_flight.html", user=current_user, form=form)


@views.route("/staff/change_status", methods=['GET', 'POST'])
@login_required
def change_status():
    if not session["account_type"] == 'staff':
        flash('You must be logged in as an airline staff for this action', "error")
        return redirect(url_for('views.index'))
    form = ChangeStatusForm()
    form.flight_number.choices = [(i.flight_number, i.flight_number) for i in db.session.query(Flight).all()]
    if form.validate_on_submit():
        flight_number = form.flight_number.data
        new_status = form.new_status.data
        flight = db.session.query(Flight).filter_by(flight_number=flight_number).first()
        flight.status = new_status
        db.session.commit()
        flash('You have updated status to ' + str(new_status))
        return redirect(url_for('views.index'))

    return render_template("staff/change_status.html", user=current_user, form=form)


@views.route("/staff/get_airplanes")
@login_required
def get_airplanes():
    if not session["account_type"] == 'staff':
        flash('You must be logged in as an airline staff for this action', "error")
        return redirect(url_for('views.index'))

    data = db.session.query(Airplane, Airline).join(Airline).all()
    return render_template("staff/get_airplanes.html", user=current_user, data=data)


@views.route("/staff/get_airports")
@login_required
def get_airports():
    if not session["account_type"] == 'staff':
        flash('You must be logged in as an airline staff for this action', "error")
        return redirect(url_for('views.index'))
    data = db.session.query(Airport).all()
    return render_template("staff/get_airports.html", user=current_user, data=data)


@views.route("/staff/get_flights")
@login_required
def get_flights():
    if not session["account_type"] == 'staff':
        flash('You must be logged in as an airline staff for this action', "error")
        return redirect(url_for('views.index'))

    # data = db.session.query(Flight).all()
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT f.flight_number, f.start_time, f.end_time, f.destination, f.source, f.capacity, f.status, a.model, a2.name destination_airport, a1.name source_aiport
    FROM flight f
    JOIN airport a1 
    ON a1.airport_code = f.airport_code_source
    JOIN airport a2
    ON a2.airport_code = f.airport_code_destination
    JOIN airplane a 
    ON a.plane_id = f.plane_id;
    """)
    data = cur.fetchall()
    cur.close()

    return render_template("staff/get_flights.html", user=current_user, data=data)


@views.route("/staff/get_bookings", methods=['GET', 'POST'])
@login_required
def get_bookings():
    if not session["account_type"] == 'staff':
        flash('You must be logged in as an airline staff for this action', "error")
        return redirect(url_for('views.index'))
    form = GetBookingsForm()
    if form.validate_on_submit():
        booking_date = form.date.data
        data = db.session.query(Booking, Customer).join(Customer).filter(
            cast(Booking.booking_time, Date) == booking_date).all()

        if data:
            return render_template("staff/bookings_result.html", user=current_user, data=data)
        else:
            flash("No bookings on this day", "error")

    return render_template("staff/get_bookings.html", user=current_user, form=form)
