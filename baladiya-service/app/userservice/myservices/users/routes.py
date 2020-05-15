from flask import request, jsonify, Blueprint, current_app, url_for, make_response, Flask
from flask_marshmallow import Marshmallow
from userservice.myservices.users.models import User
from userservice import db, bcrypt, login_manager, app
from flask_login import login_user, current_user, logout_user, login_required
from userservice.myservices.decorators import require_appkey, token_required
from userservice.myservices.session.models import Session
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from flask import render_template
from flask import send_file, send_from_directory, safe_join, abort
from flask_cors import CORS,cross_origin
import random ,werkzeug,os,jwt ,base64


#blueprint
users = Blueprint('users', __name__)
# Init marshmallow
ma = Marshmallow(users)
# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('idUser', 'firstName', 'lastName', 'email','gender' ,'phoneNumber',  'password',
                  'dateOfBirth', 'role',  'isLogged', 'isCreated','account','deleted')

# Init schema
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)


@users.route('/user', methods=['GET','POST'])
@require_appkey
@token_required
@cross_origin()
def getUser(current_user,current_session):
    if current_user.role == "admin":
        if not request.json['email']:
             email=current_user.email
        else:
            email = request.json['email']
        # Fetch user
        user = User.query.filter_by(email=email,deleted=False).first()
        if not user:
            return jsonify({'msg': 'No user found!'
                        })
        return user_schema.jsonify(user)
    return jsonify({'msg': 'No permission!'})


# Log In
@users.route("/user/login", methods=['POST'])
@require_appkey
@cross_origin()
def login():
    email = request.json['email']
    pwd = request.json['password']
    app = request.json['app']

    now = datetime.now()
    timeStamp = now.strftime("%m/%d/%Y, %H:%M:%S")
    rand = str(int(random.random() * 10000000000000000000000))
    device = werkzeug.utils.secure_filename(timeStamp + rand)
    role = 'admin'
    user = User.query.filter_by(email=email,role=role,deleted=False).first()
    if not user:
        return jsonify({'isLogged': False,
                                'msg': "User not registred or deleted!"})

    if bcrypt.check_password_hash(user.password, pwd):
        if (user.isCreated == 0):
        	return jsonify({'isLogged': False,
                        'msg': "verify"})
        user.isLogged = True
        token = jwt.encode({'idUser': user.idUser ,'exp': datetime.utcnow() + timedelta(seconds=1800)},
    		    	current_app.config['SECRET_KEY'])
        token = token.decode('UTF-8')
        now = datetime.now()
        loggedAt = now.strftime("%m/%d/%Y, %H:%M:%S")
        newSession=Session(device,user.idUser,token,loggedAt)
        db.session.add(newSession)
        db.session.commit()
        return jsonify({'isLogged': user.isLogged,
        'token':token,'msg': 'User successfully logged in !'
    		            	})
        return jsonify({
            'msg':'device is connected !'
        })
    user.isLogged = False
    return jsonify({
        'isLogged': user.isLogged,
        'msg': 'Password incorrect !'
    })
# Update user info
@users.route('/user/updateClient', methods=['GET','POST'])
@require_appkey
@token_required
@cross_origin()
def updateReact(current_user,current_session):
 if current_user.role == "admin":

    email=request.json['email']
    user=User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'msg':'not found',
                        'isUpdated': False})

    # update fields
    sexe=request.json['gender']
    if sexe=="male":
        gender=True
    else:
        gender=False
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    phoneNumber = request.json['phoneNumber']
    dateOfBirth = request.json['dateOfBirth']
    user.gender=gender
    user.firstName=firstName
    user.lastName=lastName
    user.phoneNumber=phoneNumber
    user.dateOfBirth=dateOfBirth
    db.session.commit()

    return jsonify({'msg': 'User successfully updated!',
                    'isUpdated': True})
 return jsonify({'msg': 'No permission!'})
# Update password
@users.route('/user/updatePassword', methods=['PUT'])
@require_appkey
@token_required
@cross_origin()
def updatePass(current_user,current_session):
    oldPassword = request.json['oldPassword']
    if bcrypt.check_password_hash(current_user.password, oldPassword):
        newPassword = bcrypt.generate_password_hash(request.json['newPassword']).decode('utf-8')
        current_user.password = newPassword
        return jsonify({'msg': 'password updated!',
                        'isUpdated': True})
    return jsonify({'msg': 'wrong Password',
                    'isUpdated': False})
# Get All Admins
@users.route('/admin', methods=['GET'])
@require_appkey
@token_required
@cross_origin()
def getAdmin(current_user,current_session):
    if current_user.role == "admin":
        all_users = User.query.filter_by(role="admin",deleted=False).all()
        result = users_schema.dump(all_users)
        return jsonify(result.data)
    return jsonify({'msg': 'No permission!'})


# Create account ADMIN et client web
@users.route('/user/signUpWeb', methods=['POST'])
@require_appkey
@cross_origin()
def createAccountweb():
    email = request.json['email']
    # Fetch user
    user = User.query.filter_by(email=email,deleted=False).first()
    if not user:
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        email = request.json['email']
        sexe = request.json['gender']
        if sexe=="male":
            gender = True
        else:
            gender = False
        phoneNumber = request.json['phoneNumber']
        codeReset = str(int(random.random() * 100000))
        pwd = request.json['password']
        password = bcrypt.generate_password_hash (pwd).decode ('utf-8')
        dateOfBirth = request.json['dateOfBirth']
        role = request.json['role']
        account = "normal"
        new_user = User(firstName, lastName, email,gender, phoneNumber,  password,
                        dateOfBirth, role,account)
        db.session.add(new_user)
        db.session.commit()
        newAdmin= User.query.filter_by(email=email,deleted=False).first()
        newAdmin.isCreated=True
        return jsonify({
            'msgMail':True,
            'check': True ,
            'msg': 'New account successfully created !'
        })
    else:
        return jsonify({
            'msgMail':False,
            'check': False,
            'msg': 'Email address is already registred !'
    })
# Logout
@users.route("/user/logOut", methods=['POST'])
@require_appkey
@token_required
@cross_origin()
def logout(current_user,current_session):
    db.session.delete(current_session)
    db.session.commit()
    session = Session.query.filter_by(idUser=current_user.idUser).first()
    if not session:
        current_user.isLogged=False
    logout_user()
    return jsonify({
        'isLogged': 'false',
        'msg': 'User successfully logged out !'
    })
# Delete user
@users.route('/user/delete', methods=['PUT'])
@require_appkey
@token_required
@cross_origin()
def deleteUser(current_user,current_session):
    if current_user.role == "admin":
        email = request.json['email']
        # fetch user
        user = User.query.filter_by(email=email,deleted=False).first()
        if not user:
            return jsonify({'msg': 'No user found !'})
        user.deleted=True
        return jsonify({'msg': 'User has been deleted !',
        'mail':email,
        'del':user.deleted})
    return jsonify({'msg': 'not permission !' })
