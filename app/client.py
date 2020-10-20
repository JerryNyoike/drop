from os.path import join
from flask import Blueprint, request, make_response, current_app, render_template, redirect, session, url_for
from . import db
import jwt
from datetime import datetime, timedelta
from .helpers import string_hash, is_logged_in, log_error
from markupsafe import escape
from re import sub


bp = Blueprint('client', __name__, url_prefix='/client')


@bp.route('register', methods=['GET', 'POST'])
def register():
    """
    Registers the client and redirects to login page if successful
    """
    if request.method == 'POST':
        if not ('multipart/form-data' in request.content_type):
            return render_template('register.html', page="Register", error="Bad Request"), 400

        user_data = request.form
        if user_exists(user_data['email'])[0]:
            return render_template('register.html', page="Register", error="The email is already in use"), 409

        filename = "default_profile.png"
        if request.files['file']:               
            f = request.files['file']
            filename = f.filename
            f.save(join(current_app.config["PHOTO_DIR"], f.filename))
        
        result = register_user(filename, user_data)
        if not result:
            return render_template('register.html', page="Register", error="Something went wrong. Try again later"), 409
        return render_template('login.html', success="Registration successful. Login Here")

    return render_template('register.html', page="Register"), 200


@bp.route('login', methods=['GET', 'POST'])
def login():
    """
    Saves a json web token to the client which is used
    to verify all other queries made by the client
    """
    if request.method == 'POST':
        
        if request.content_type != 'application/json':
            return render_template('login.html', page="Login", error="Content type needs to be application/json"), 400

        request_data = request.get_json()
        user_data = fetch_user(request_data["email"], request_data["pwd"])
        if not user_data:
            return render_template('login.html', page="Login", error="The user doesn\'t exist"), 404

        # create token and return it to client side
        expiration = datetime.now() + timedelta(days=10)
        token = jwt.encode(
                {
                    'typ': 'client', 
                    'exp': expiration, 
                    'sub': user_data['c_id']		
                }, current_app.config['SCRT'], algorithm='HS256').decode('utf-8')
        del user_data['c_id']
        response = make_response({"status": 1, "message": "Login successful", "user_details": user_data}, 200)
        response.set_cookie('token', token, expires=expiration, secure=True, httponly=True, samesite='Lax')
        return response

    return render_template('login.html', page="Login"), 200


@bp.route('reset-password', methods=['POST'])
def resetPasswordRequest():
    request_info = request.get_json()
    user_id = user_exists(request_info['email'])[-1]
    token = createToken(user_id, 'client')
    # TODO write code to send user an email




@bp.route('reset/password/<token>', methods=['GET', 'POST'])
def reset_pwd(token):
    if not token:
        return redirect(url_for('client.login'), 401)

    request_data = request.form
    user_info = is_logged_in(token)
    if token['typ'] != 'client':
        return render_template('login.html', page="Login", error="Login as a client for this action"), 200
     
    changePasswordQuery = '''UPDATE client SET pwd = {} WHERE c_id = UUID_TO_BIN("{}")'''.format(string_hash(request_data['new_pwd']), user_info['sub'])
    conn = db.get_db()
    cur = conn.cursor()
    result = cur.execute(changePasswordQuery)
    if result == 1:
        return render_template('reset_pwd.html', page="Reset Password"), 200
    else:
        return render_template('reset_pwd.html', page="Reset Password"), 200


@bp.route('profile', methods=['GET', 'PATCH'])
def profile():
    crumbs = [
        {"name": "Home", "url": url_for('routes.index'), "active": "true"}
    ]

    token = is_logged_in(request.cookies.get('token'))
    if not token:
        return redirect(url_for('.login'), 401)

    if token['typ'] != 'client':
        return render_template('login.html', page="Login", error="Login as client for this action"), 200

    if request.method == 'PATCH':
        conn = db.get_db()
        cur = conn.cursor()
        
        request_data = request.form
        addClientDetailsQuery = '''UPDATE client_profile SET bio={}, profession={}, address={}, city={} WHERE client_id=UUID_TO_BIN("{}")'''.format(request_data["bio"], request_data["profession"], request_data["address"], request_data["city"], token["sub"])

        result = cur.execute(addClientDetailsQuery)
        conn.commit()

        if result == 1:
            return render_template('settings.html', page="Settings", crumbs=crumbs, producer=producer), 200
        else:
            return render_template('settings.html', page="Settings", crumbs=crumbs, producer=producer), 500
    else:
        client_query = '''SELECT (BIN_TO_UUID(client.c_id)) client_id, client.profile_image, client.email, client.name, client.phone_number, client_profile.bio, 
    client_profile.profession, client_profile.address, client_profile.city FROM client LEFT JOIN client_profile ON client.c_id = client_profile.client_id WHERE client.c_id = UUID_TO_BIN("{}")'''.format(escape(token['sub']))

    cur.execute(client_query) 
    client = cur.fetchone()

    if not client:
        return redirect(url_for('.login'), 401)

    return render_template('client_profile.html', page=client["name"], crumbs=crumbs, client=client), 200


@bp.route('cart', methods=['GET'])
def cart():
    crumbs = [
        {"name": "Home", "url": url_for('routes.index'), "active": "true"}
    ]
    return render_template('cart.html', page="Cart", crumbs=crumbs), 200


@bp.route('yourbeats', methods=['GET'])
def yourbeats():
    crumbs = [
        {"name": "Home", "url": url_for('routes.index'), "active": "true"}
    ]
    return render_template('yourbeats.html', page="Your Beats", crumbs=crumbs), 200


@bp.route('settings', methods=['GET'])
def settings():
    crumbs = [
        {"name": "Home", "url": url_for('routes.index'), "active": "true"}
    ]

    token = is_logged_in(request.cookies.get('token'))
    if not token:
        return redirect(url_for('.login'), 401)

    if token['typ'] != 'client':
        return render_template('login.html', page="Login", error="Login as client for this action"), 200

    client_query = '''SELECT (BIN_TO_UUID(c.c_id)) client_id, c.profile_image, c.email, c.name, c.phone_number, cp.bio, cp.profession, cp.address, cp.city FROM client c INNER JOIN client_profile cp ON c.c_id = cp.client_id WHERE c.c_id = UUID_TO_BIN("{}")'''.format(escape(token['sub']))

    conn = db.get_db()
    cur = conn.cursor()

    cur.execute(client_query) 
    client = cur.fetchone()

    if not client:
        return render_template('login.html', page="Login", error="Login for this action"), 200

    return render_template('settings.html', page="Settings", crumbs=crumbs, client=client), 200


@bp.route('logout', methods=['GET'])
def logout():
    token = is_logged_in(request.cookies.get('token'))
    if not token:
        return redirect(url_for('.login'), 401)

    if token['typ'] != 'client':
        return render_template('login.html', page="Login", error="Login as client for this action"), 200

    response = make_response({"status": 1, "message": "Successful"}, 200)
    response.set_cookie('token', '', secure=True, httponly=True, samesite='Lax')
    return response


def register_user(filename, user_data):
    conn = db.get_db()
    cur = conn.cursor()

    # phone_number = sub(r"^[^0-9-]$", user_data['phone'], '')
    query = '''INSERT INTO client (c_id, email, phone_number, name, pwd, profile_image)
            VALUES (UUID_TO_BIN(UUID()), '{}', {}, '{}', '{}', '{}')'''.format(
                user_data['email'], user_data['phone'], user_data['name'], string_hash(user_data['pwd']), filename
            )

    result = cur.execute(query)
    conn.commit()
    return result


def user_exists(email):
    cur = db.get_db().cursor()

    query = "SELECT (BIN_TO_UUID(c_id) client_id) FROM client WHERE email = '%s' LIMIT 1" % email
    cur.execute(query)
    result = cur.fetchone()

    if not result:
        return False, None
    return True, result


def fetch_user(email, pwd):
    cur = db.get_db().cursor()
    query = "SELECT BIN_TO_UUID(c_id) c_id, profile_image, name FROM client WHERE `email` = '{}' AND `pwd` = '{}' LIMIT 1".format(
            email, string_hash(pwd)
        )
    cur.execute(query)
    result = cur.fetchone()
    return result

