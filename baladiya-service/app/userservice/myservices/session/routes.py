from flask import request, jsonify, Blueprint, current_app, url_for, make_response
from flask_marshmallow import Marshmallow
from userservice.myservices.session.models  import Session
from userservice import db, bcrypt, login_manager, app
from flask_login import login_user, current_user, logout_user, login_required
from userservice.myservices.decorators import require_appkey, token_required
from userservice.myservices.users.models import User
from datetime import datetime
from flask_cors import CORS,cross_origin
import jwt

#blueprint
session = Blueprint('session', __name__)

# Init marshmallow
ma = Marshmallow(session)

# User Schema
class SessionSchema(ma.Schema):
  class Meta:
    fields = ('idSession','device','token','idUser','loggedAt')

# Init schema
sessionschema = SessionSchema(strict=True)
session_schema = SessionSchema(many=True, strict=True)

#get all Session
@session.route('/session', methods=['GET'])
@require_appkey
@cross_origin()
def getSession():
        all_session =Session.query.all()
        result = session_schema.dump(all_session)
        return jsonify(result.data)
