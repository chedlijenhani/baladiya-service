from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, types
from datetime import datetime
from userservice import db
from werkzeug import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin




# Registred User Class/Model

class User(UserMixin, db.Model):
    idUser = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.Boolean,unique=False, default=False)
    phoneNumber = db.Column(db.String(20), unique=False, nullable=False)
    password= db.Column(db.String(60), nullable=False)
    dateOfBirth = db.Column(db.String(60), nullable=False)
    role=db.Column(db.String(60), nullable=False)
    account = db.Column(db.String(150), nullable = False)
    isLogged = db.Column(db.Boolean,unique=False, default=False)
    isCreated = db.Column(db.Boolean,unique=False, default=False)
    deleted = db.Column(db.Boolean, nullable = True,default=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    # Init constructorlevelConfidence_user,
    def __init__(self, firstName, lastName, email,gender, phoneNumber, password, dateOfBirth, role,account):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.gender = gender
        self.phoneNumber = phoneNumber
        self.password = password
        self.dateOfBirth = dateOfBirth
        self.role = role
        self.account = account
