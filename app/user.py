from os.path import join
from flask import Blueprint, request, current_app, render_template, redirect, session
from . import db
import jwt
from datetime import datetime, timedelta
from .helpers import string_hash, log_error


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.content_type != 'application/json':
            session["error"] = "Content type needs to be application/json"
            return render_template('register.html', page="Login"), 400

        request_data = request.get_json()
        if user_exists(request_data['email']):
            session["error"] = "The email is already in use"
            return render_template('register.html', page="Register"), 409

        result = register_user(request_data)
        if not result:
            session["error"] = "Something went wrong. Try again later"
            return render_template('register.html', page="Register"), 409
        return redirect(url_for('.login'))

    return render_template('register.html', page="Register"), 200


@bp.route('login', methods=['GET', 'POST'])
def login():
    """
    Returns a json web token to the client which is used
    to verify all other queries made by the client
    """
    if request.method == 'POST':
        if request.content_type != 'application/json':
            session["error"] = "Content type needs to be application/json"
            return render_template('login.html', page="Login"), 200

        request_data = request.get_json()
        user_data = fetch_user(request_data["email"], request_data["pwd"])
        if not user_data:
            session["error"] = "The user does not exist"
            return render_template('login.html', page="Login"), 200

        # create token and return it to client side
        token = jwt.encode(
                {
                    'typ': 'client', 
                    'exp': datetime.now() + timedelta(days=10), 
                    'sub': user_data['c_id']		
                }, current_app.config['SCRT'], algorithm='HS256').decode('utf-8')
        session["success"] = "Login successful"
        response = make_response({'success': 1, 'message': 'Login successful'}, 200)
        response.set_cookie('token', token)
        return response

    return render_template('login.html', page="Login"), 200


@bp.route('reset/password', methods=['GET', 'POST'])
def reset_pwd():
    return render_template('reset_pwd.html'), 200


def register_user(user_data):
    conn = db.get_db()
    cur = conn.cursor()

    query = "INSERT INTO client (c_id, email, phone_number, name, pwd) VALUES (UUID_TO_BIN(UUID()), '{}', {}, '{}', '{}')".format(
        user_data['email'], user_data['phone'], user_data['name'], string_hash(user_data['pwd']))

    result = cur.execute(query)
    conn.commit()
    return result


def user_exists(email):
    cur = db.get_db().cursor()

    query = "SELECT (BIN_TO_UUID(c_id)) FROM client WHERE email = '%s' LIMIT 1" % email
    cur.execute(query)
    result = cur.fetchone()

    if not result:
        return False
    return True


def fetch_user(email, pwd):
    cur = db.get_db().cursor()
    query = "SELECT BIN_TO_UUID(c_id) c_id, email, name FROM client WHERE `email` = '{}' AND `pwd` = '{}' LIMIT 1".format(
            email, string_hash(pwd)
        )
    cur.execute(query)
    result = cur.fetchone()
    return result

