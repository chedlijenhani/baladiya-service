from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, types,JSON,Float
from datetime import datetime
from userservice import db
from werkzeug import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin




# Article Model

class Article(UserMixin,db.Model):
    idArticle = db.Column(db.Integer, primary_key=True)
    nameArticle=db.Column(db.String(200))
    description=db.Column(db.String(256))
    imageArticle=db.Column(db.String(256))
    dateCreated=db.Column(db.String(256))
    dateEnd=db.Column(db.String(256))

    # Init constructor
    def __init__(self,nameArticle,description,imageArticle,dateCreated,dateEnd):
        self.nameArticle=nameArticle
        self.description=description
        self.imageArticle=imageArticle
        self.dateCreated=dateCreated
        self.dateEnd=dateEnd
