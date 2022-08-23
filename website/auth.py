from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Customer, Staff
from . import db, bcrypt
from flask_login import login_user, login_required, logout_user, current_user

from .forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_type = form.type.data
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        if user_type == "customer":
            customer = db.session.query(Customer).filter_by(email=email).first()
            if customer and bcrypt.check_password_hash(customer.password, password):
                session["account_type"] = "customer"
                login_user(customer, remember=remember)
                return redirect(url_for("views.index"))
            else:
                flash('Login Unsuccessful. Please check email and password', 'error')
        elif user_type == "staff":
            staff = db.session.query(Staff).filter_by(email=email).first()
            if staff and bcrypt.check_password_hash(staff.password, password):
                session["account_type"] = "staff"
                login_user(staff, remember=remember)
                return redirect(url_for("views.index"))
            else:
                flash('Login Unsuccessful. Please check email and password', 'error')

    return render_template('login.html', form=form, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        type_ = form.type.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        if type_ == "customer":
            customer = Customer(email=email, password=hashed_password, first_name=first_name, last_name=last_name)
            db.session.add(customer)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('auth.login'))
        elif type_ == "staff":
            staff = Staff(email=email, password=hashed_password, first_name=first_name, last_name=last_name)
            db.session.add(staff)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', form=form, user=current_user)
