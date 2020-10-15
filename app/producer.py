from os.path import join
from flask import Blueprint, request, make_response, current_app, render_template, redirect, session, url_for
from . import db
import jwt
from datetime import datetime, timedelta
from .helpers import string_hash, is_logged_in, log_error
from markupsafe import escape
from re import sub


bp = Blueprint('producer', __name__, url_prefix='/producer')


@bp.route('dashboard', methods=['GET'])
def dashboard():
    return render_template("dashboard/index.html", page="Dashboard"), 200


@bp.route('register', methods=['GET', 'POST'])
def register():
    """
    Registers the producer and redirects to login page if successful
    """
    if request.method == 'POST':
        if not ('multipart/form-data' in request.content_type):
            return render_template('dashboard/register.html', page="Register", error="Bad Request"), 400

        user_data = request.form
        if user_exists(user_data['email']):
            return render_template('dashboard/register.html', page="Register", error="The email is already in use"), 409

        filename = "default_profile.png"
        if request.files['file']:               
            f = request.files['file']
            filename = f.filename
            f.save(join(current_app.config["PHOTO_DIR"], f.filename))
        
        result = register_user(filename, user_data)
        if not result:
            return render_template('dashboard/register.html', page="Register", error="Something went wrong. Try again later"), 409
        return redirect(url_for('.login'), code=401)

    return render_template('dashboard/register.html', page="Register"), 200


@bp.route('login', methods=['GET', 'POST'])
def login():
    """
    Saves a json web token to the producer which is used
    to verify all other queries made by the producer
    """
    if request.method == 'POST':
        if request.content_type != 'application/json':
            return render_template('dashboard/login.html', page="Login", error="Content type needs to be application/json"), 400

        request_data = request.get_json()
        user_data = fetch_user(request_data["email"], request_data["pwd"])
        if not user_data:
            return render_template('dashboard/login.html', page="Login", error="The user doesn\'t exist"), 404

        # create token and return it to producer side
        expiration = datetime.now() + timedelta(days=10)
        token = jwt.encode(
                {
                    'typ': 'producer', 
                    'exp': expiration, 
                    'sub': user_data['BIN_TO_UUID(producer_id)']		
                }, current_app.config['SCRT'], algorithm='HS256').decode('utf-8')
        del user_data['BIN_TO_UUID(producer_id)']
        response = make_response({"status": 1, "message": "Login successful", "user_details": user_data}, 200)
        response.set_cookie('token', token, expires=expiration, secure=True, httponly=True, samesite='Lax')
        return response

    return render_template('dashboard/login.html', page="Login"), 200


@bp.route('reset/password', methods=['GET', 'POST'])
def reset_pwd():
    # token = is_logged_in(request.cookies.get('token'))

    # if not token:
    #     return redirect(url_for('producer.login'), 401)

    user_data = request.form
    # if token['typ'] != 'producer':
    #     return render_template('login.html', page="Login", error="Login as producer for this action"), 200
     
    # TODO: Send email function

    return render_template('dashboard/reset_pwd.html', page="Reset Password"), 200


@bp.route('verify/password', methods=['GET', 'POST'])
def verify_pwd():
    if request.method == 'POST':
        # token = is_logged_in(request.cookies.get('token'))

        # if not token:
        #     return redirect(url_for('producer.login'), 401)

        user_data = request.form
        # if token['typ'] != 'producer':
        #     return render_template('login.html', page="Login", error="Login as producer for this action"), 200
        
        changePasswordQuery = '''UPDATE producer SET pwd = {} WHERE producer_id = UUID_TO_BIN("{}")'''.format(string_hash(user_data['new_pwd']), token)
    
    return render_template('dashboard/verify_pwd.html', page="Reset Password"), 200


@bp.route('beats', methods=['GET'])
def beats():    
    token = is_logged_in(request.cookies.get('token'))

    if not token:
        return redirect(url_for('.login'), code=401)
    
    crumbs = [
        {"name": "Home", "url": url_for('.dashboard')}
    ]

    return render_template('dashboard/beats.html', page="Your Beats", crumbs=crumbs), 200


@bp.route('upload/beat', methods=['GET'])
def upload_beat():    
    token = is_logged_in(request.cookies.get('token'))

    if not token:
        return redirect(url_for('.login'), code=401)

    return render_template('dashboard/upload.html', page="Upload Beat"), 200


@bp.route('<producer_id>', methods=['GET'])
def producer_profile(producer_id):
    crumbs = [
        {"name": "Home", "url": url_for('routes.index'), "active": "true"}
    ]  

    token = is_logged_in(request.cookies.get('token'))
    if not token:
        return redirect(url_for('.login'), code=401)

    producer_query = '''SELECT (BIN_TO_UUID(producer.producer_id)) producer_id, producer.profile_image, producer.email, producer.name, producer.phone_number, producer_profile.bio, producer_profile.profession, producer_profile.address, producer_profile.city FROM producer LEFT JOIN producer_profile ON producer.producer_id = producer_profile.producer_id WHERE producer.producer_id = UUID_TO_BIN("{}")'''.format(escape(producer_id))

    beats_query = '''SELECT (BIN_TO_UUID(beat_id)) beat_id, name, upload_date FROM beat WHERE 
    producer_id = UUID_TO_BIN("{}")'''.format(escape(producer_id))

    conn = db.get_db()
    cur = conn.cursor()

    cur.execute(producer_query) 
    producer = cur.fetchone()

    cur.execute(beats_query)
    beats = cur.fetchall()

    if not producer:
        return render_template('producer_profile.html'), 404

    return render_template('producer_profile.html', page=producer["name"], crumbs=crumbs, producer=producer, beats=beats), 200


@bp.route('yourbeats', methods=['GET'])
def yourbeats():
    token = is_logged_in(request.cookies.get('token'))
    if not token:
        return redirect(url_for('.login'), 401)

    crumbs = [
        {"name": "Home", "url": url_for('.dashboard'), "active": "false"}
    ]

    return render_template('yourbeats.html', page="Your Beats", crumbs=crumbs), 200


@bp.route('settings', methods=['GET'])
def settings():
    crumbs = [
        {"name": "Home", "url": url_for('.dashboard'), "active": "false"}
    ]

    token = is_logged_in(request.cookies.get('token'))
    if not token:
        return redirect(url_for('.login'), code=401)

    if token['typ'] != 'producer':
        return render_template('login.html', page="Login", error="Login as producer for this action"), 401

    producerProfileQuery = '''SELECT (BIN_TO_UUID(producer.producer_id)) producer_id, producer.profile_image, producer.email, producer.name, producer.phone_number, producer_profile.bio, producer_profile.profession, producer_profile.address, producer_profile.city FROM producer LEFT JOIN producer_profile ON producer.producer_id = producer_profile.producer_id WHERE producer.producer_id = UUID_TO_BIN("{}")'''.format(escape(token['sub']))

    conn = db.get_db()
    cur = conn.cursor()

    cur.execute(producerProfileQuery) 
    producer = cur.fetchone()

    if not producer:
        return redirect(url_for('.login'), code=401)

    return render_template('settings.html', page="Settings", crumbs=crumbs, producer=producer), 200


@bp.route('logout', methods=['GET'])
def logout():
    token = is_logged_in(request.cookies.get('token'))
    print(token)

    token = is_logged_in(request.cookies.get('token'))
    if not token:
        return redirect(url_for('producer.login'), 401)

    if token['typ'] != 'producer':
        return render_template('login.html', page="Login", error="Login as producer for this action"), 200

    response = make_response({"status": 1, "message": "Successful"}, 200)
    response.set_cookie('token', '', secure=True, httponly=True, samesite='Lax')
    return response


def register_user(filename, user_data):
    conn = db.get_db()
    cur = conn.cursor()

    # phone_number = sub(r"^[^0-9-]$", user_data['phone'], '')
    registerQuery = '''INSERT INTO producer (producer_id, email, phone_number, name, pwd, profile_image) 
                    VALUES (UUID_TO_BIN(UUID()), '{}', {}, '{}', '{}', '{}')'''.format(
                        user_data['email'], user_data['phone'], user_data['name'], string_hash(user_data['pwd']), filename
                    )
    registerResult = cur.execute(registerQuery)
    conn.commit()
    if registerResult == 1:
        prod = fetch_user(user_data['email'], user_data['pwd'])
        createProfileQuery = '''INSERT INTO producer_profile (profile_id, producer_id, bio, profession, address, city) VALUES (UUID_TO_BIN(UUID()), UUID_TO_BIN("{}"), '', '', '', '')'''.format(prod['BIN_TO_UUID(producer_id)'])
        # create the profile
        profileCreationResult = cur.execute(createProfileQuery)
        conn.commit()
    return registerResult


def user_exists(email):
    cur = db.get_db().cursor()

    query = "SELECT (BIN_TO_UUID(producer_id)) FROM producer WHERE email = '%s' LIMIT 1" % email
    cur.execute(query)
    result = cur.fetchone()

    if not result:
        return False
    return True


def fetch_user(email, pwd):
    cur = db.get_db().cursor()
    query = "SELECT BIN_TO_UUID(producer_id), profile_image, name FROM producer WHERE `email` = '{}' AND `pwd` = '{}' LIMIT 1".format(
            email, string_hash(pwd)
        )
    cur.execute(query)
    result = cur.fetchone()
    return result

