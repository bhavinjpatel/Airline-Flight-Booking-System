from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, IntegerField, \
    DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from .models import Customer
from .models import Staff


class LoginForm(FlaskForm):
    type = SelectField(u'Account type', choices=[('customer', 'Customer'), ('staff', 'Staff')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    type = SelectField(u'Account type', choices=[('customer', 'Customer'), ('staff', 'Staff')])
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if self.type.data == "customer":
            user = Customer.query.filter_by(email=email.data).first()
        elif self.type.data == "staff":
            user = Staff.query.filter_by(email=email.data).first()
        else:
            return
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class SearchFlightForm(FlaskForm):
    source_city = SelectField('Source City')
    dest_city = SelectField('Destination City')
    # source_airport = SelectField('Source Airport', validators=[])
    # dest_airport = SelectField('Destination Airport')
    flight_date = DateField('Flight Date', validators=[DataRequired(message='dd/mm/yyyy')])
    submit = SubmitField('Search')

    def validate_dest_city(self, city):
        if city.data == self.source_city.data:
            raise ValidationError("Destination city must be different.")


class BookFlightForm(FlaskForm):
    flight_number = SelectField('Flight number', validators=[DataRequired('Please select flight number')])
    seats = IntegerField('Seats', default=1, validators=[NumberRange(min=1, max=10)])
    submit = SubmitField('Book')


class AddAirplaneForm(FlaskForm):
    model = StringField('Model', validators=[DataRequired(message='Mandatory')])
    airline_name = SelectField('Airline Name', validators=[DataRequired(message='Mandatory')])
    submit = SubmitField('Add Airplane')


class AddFlightForm(FlaskForm):
    start_time = DateTimeLocalField('Flight Departure Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    end_time = DateTimeLocalField('Flight Arrival Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    destination = SelectField('Destination City', validators=[DataRequired(message='Mandatory')])
    source = SelectField('Source City', validators=[DataRequired(message='Mandatory')])
    capacity = IntegerField('Flight Capacity', validators=[DataRequired(message='Mandatory')])
    status = StringField('Flight Status', validators=[DataRequired(message='Mandatory')])
    airplane = SelectField('Airplane', validators=[DataRequired(message='Mandatory')])
    airport_destination = SelectField('Destination Airport', validators=[DataRequired(message='Mandatory')])
    airport_source = SelectField('Source Airport', validators=[DataRequired(message='Mandatory')])
    submit = SubmitField('Add Flight')


class AddAirportForm(FlaskForm):
    country = StringField('Airport Country', validators=[DataRequired(), Length(3, 3)])
    city = StringField('City', validators=[DataRequired()])
    name = StringField('Airport Name', validators=[DataRequired(), Length(3, 3)])
    submit = SubmitField('Add Airport')


class ChangeStatusForm(FlaskForm):
    flight_number = SelectField('Flight number', validators=[DataRequired(message='Mandatory')])
    new_status = StringField('New Status', validators=[DataRequired(message='Mandatory')])
    submit = SubmitField('Change Status')


class GetBookingsForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired(message='dd/mm/yyyy')])
    submit = SubmitField('Get')
