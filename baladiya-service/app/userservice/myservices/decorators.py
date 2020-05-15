from functools import wraps
from flask import request, abort, jsonify
from userservice import app
from flask_login import login_user, current_user
from userservice.myservices.users.models import User
from userservice.myservices.session.models import Session
import jwt,ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('static/api_key_files/server.crt', 'static/api_key_files/server.key')

# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        with open('static/api_key_files/api.key', 'r') as apikey:
            key=apikey.read().replace('\n', '')
        #if request.args.get('key') and request.args.get('key') == key:
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == key:
            return view_function(*args, **kwargs)
        else:
            #abort(401)
            return jsonify ({ 'msg': '401:Unauthorized, API key is missing !'

                             })
    return decorated_function


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            #data = jwt.decode(token, app.config['SECRET_KEY'])
            current_session = Session.query.filter_by(token=token).first()
            if current_session is None:
                return jsonify({'message' : 'isLogged is false!'})

            current_user = User.query.filter_by(idUser=current_session.idUser).first()
            if current_user is None:
                return jsonify({'message' : 'user is invalid!'})
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user,current_session, *args, **kwargs)

    return decorated
