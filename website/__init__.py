import yaml
from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL

db = SQLAlchemy()
DB_NAME = "database.db"
bcrypt = Bcrypt()
mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    db_conf = yaml.safe_load(open('db_conf.yaml'))
    host = db_conf['mysql_host']
    user = db_conf['mysql_user']
    password = db_conf['mysql_password']
    db_name = db_conf['mysql_db']

    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_USER'] = user
    app.config['MYSQL_PASSWORD'] = password
    app.config['MYSQL_DB'] = db_name

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{user}:{password}@{host}/{db_name}"

    db.init_app(app)
    mysql.init_app(app)
    bcrypt.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Customer, Staff

    db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    Bootstrap(app)

    @login_manager.user_loader
    def load_user(id):
        if session['account_type'] == 'customer':
            return Customer.query.get(int(id))
        elif session['account_type'] == 'staff':
            return Staff.query.get(int(id))
        else:
            return None

    return app
