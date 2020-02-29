from flask import Blueprint, request, make_response, current_app
from . import db
import jwt
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('register', methods=['POST'])
def register():
    if request.content_type == 'application/json':
        request_data = request.get_json()
        if not user_exists(request_data['type'], request_data['email']):
            result = register_user(request_data)
            if result is not None:
                return make_response({'status': 1, 'message': 'Registration successful'})
            else:
                print(result)
                return make_response({'status': 0, 'message': 'Registration unsuccessful'})
        else:
            return make_response({'status': 0, 'message': 'User already exists'}, 400)
    else:
        return make_response({'status': 0, 'message': 'Invalid content type'}, 400)


@bp.route('login', methods=['POST'])
def login():
    """Returns a json web token to the client which is used
    to verify all other queries made by the client
    """
    if request.content_type == 'application/json':
        request_data = request.get_json()
        user_data = fetch_user(request_data)
        if user_data is not None:
            # create token and return it to client side
            token = jwt.encode({'aud': request_data['type'], 'exp': datetime.now() + timedelta(days=10)},
                               current_app.config['SCRT'], algorithm='HS256').decode('utf-8')
            return make_response({'status': 1, 'message': 'Successful login', 'payload': token})
        else:
            return make_response({'status': 0, 'message': 'User does not exist'})
    else:
        return make_response({'status': 0, 'message': 'Content type needs to be application/json'})


def register_user(user_data):
    conn = db.get_db()
    cur = conn.cursor()
    table, uid = db_info(user_data['type'])

    query = "INSERT INTO {} ({}, email, phone_number, name, pwd) VALUES (UUID_TO_BIN(UUID()), '{}', {}, '{}', '{}')".format(
        table, uid, user_data['email'], user_data['phone'], user_data['name'], user_data['pwd'])

    result = cur.execute(query)
    conn.commit()
    return result


def user_exists(user_type, email):
    cur = db.get_db().cursor()
    table, uid = db_info(user_type)

    query = "SELECT * FROM {} WHERE email = '{}' LIMIT 1".format(table, email)
    print(query)
    cur.execute(query)
    result = cur.fetchone()
    if result is not None:
        return True

    return False


def fetch_user(request_data):
    cur = db.get_db().cursor()
    table, uid = db_info(request_data['type'])

    query = "SELECT * FROM {} WHERE `email` = '{}' AND `pwd` = '{}' LIMIT 1".format(
        table, request_data['email'], request_data['pwd'])
    cur.execute(query)
    return cur.fetchone()


def is_logged_in(token):
    try:
        return jwt.decode(token, current_app.config['SCRT'], algorithm='HS256')
    except jwt.exceptions.DecodeError as e:
        return False


def db_info(user_type):
    if user_type == 'client':
        return 'client', 'c_id'

    return 'producer', 'producer_id'
