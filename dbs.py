from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager,UserMixin
import bcrypt
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
db = SQLAlchemy(app)



class Hospital(db.Model):
    __tablename__ = 'hospitals'

    hospital_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    contact_info = db.Column(db.String(100))


class Specialty(db.Model):
    __tablename__ = 'specialties'

    specialty_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)


class Doctor(db.Model):
    __tablename__ = 'doctors'

    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100))
    specialty_id = db.Column(
        db.Integer, db.ForeignKey('specialties.specialty_id'))

    specialty = db.relationship('Specialty', backref='doctors')


class Patient(db.Model):
    __tablename__ = 'patients'

    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    # Required method for Flask-Login
    def is_authenticated(self):
        return True

    # Required method for Flask-Login
    def is_active(self):
        return True

    # Required method for Flask-Login
    def is_anonymous(self):
        return False

    # Required method for Flask-Login
    def get_id(self):
        return str(self.id)


class UserRole(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))

    user = db.relationship('User', backref='user_roles')
    role = db.relationship('Role', backref='user_roles')


class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)



# Create all database tables
with app.app_context():
    db.create_all()
