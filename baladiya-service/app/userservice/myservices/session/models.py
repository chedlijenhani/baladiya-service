from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, types,JSON,Float
from datetime import datetime
from userservice import db
from werkzeug import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin




# Session Model

class Session(UserMixin,db.Model):
    idSession = db.Column(db.Integer, primary_key=True)
    device=db.Column(db.String(200))
    token=db.Column(db.String(256))
    idUser = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=True,default='NULL')
    loggedAt=db.Column(db.String(256))

    # Init constructor
    def __init__(self,device,idUser,token,loggedAt):
        self.device=device
        self.token=token
        self.idUser=idUser
        self.loggedAt=loggedAt
