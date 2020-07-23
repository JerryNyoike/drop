from flask import Blueprint, current_app, render_template, url_for, redirect, session, send_from_directory
from markupsafe import escape
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
from . import db


bp = Blueprint('routes', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
	return render_template('index.html', page="Home"), 200


@bp.route('discover', methods=['GET'])
def discover():
	return render_template('discover.html', page="Discover"), 200


@bp.route('suggestions', methods=['GET'])
def suggestions():
    return render_template('suggestions.html', page="For You"), 200


@bp.route('about', methods=['GET'])
def about():
	return render_template('about.html', page="About"), 200


@bp.route('produce', methods=['GET'])
def produce():
	return render_template('produce.html', page="Produce"), 200


@bp.route('contacts', methods=['GET'])
def contacts():
	return render_template('contacts.html', page="Contacts"), 200


@bp.route('premium', methods=['GET'])
def premium():
    return render_template('premium.html', page="Try Premium"), 200

@bp.route('producer/<producer_id>', methods=['GET'])
def producer_profile(producer_id):
    crumbs = [
        {"name": "Home", "url": url_for('.index')}
    ]

    producer_query = '''SELECT (BIN_TO_UUID(producer_id)) producer_id, profile_image, email, name, phone_number 
    FROM producer WHERE producer_id = UUID_TO_BIN("{}")'''.format(escape(producer_id))

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


@bp.route('resource/beat/<filename>', methods=['GET'])
def uploaded_beat(filename):
    return send_from_directory(current_app.config['BEAT_DIR'], secure_filename(filename))


@bp.route('resource/preview/<filename>', methods=['GET'])
def uploaded_preview(filename):
    return send_from_directory(current_app.config['PREVIEW_DIR'], secure_filename(filename))


@bp.route('resource/images/<filename>', methods=['GET'])
def uploaded_image(filename):
    return send_from_directory(current_app.config['PHOTO_DIR'], secure_filename(filename))


@bp.errorhandler(HTTPException)
def error_handler(e):
    return render_template("error_handler.html", page="Not Found", error=e.code, message=e.name), e.code
