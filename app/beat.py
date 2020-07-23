from os import path, makedirs
from pydub import AudioSegment
from pydub.utils import which
import pymysql
from flask import Blueprint, make_response, url_for, render_template, request, current_app
from werkzeug.utils import secure_filename
from hashlib import md5  
from asyncio import run
from . import db
from .routines import main
from .auth import is_logged_in
from datetime import datetime
from .helpers import log_error
from markupsafe import escape


bp = Blueprint('beat', __name__, url_prefix='/beat')

AudioSegment.converter = which("ffmpeg")

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def crop_beat(beat_path):
    '''
    This function slices a beat to just the first 30
    seconds and saves the preview to the file system and
    returns the path to the preview.
    '''
    preview_name = beat_path.split('\\')[-1]
    extension = preview_name.split('.')[-1]
    if extension in current_app.config['ALLOWED_EXTENSIONS']:
        beat = AudioSegment.from_file(beat_path, format=extension)

        # slice the audio to the first 30 seconds
        preview = beat[:30000]

        # save preview to the file system
        filename = path.join(current_app.config['PREVIEW_DIR'], preview_name)

        preview.export(filename, format='mp3')


@bp.route('beat/upload', methods=['POST'])
def insertBeat():
    if 'multipart/form-data' in request.content_type:
        token = request.cookies.get('token')
        user_info = is_logged_in(token)
        
        if user_info is not None and user_info['typ'] == 'producer':
            if 'file' in request.files:
                beat = request.files['file']

                if allowed_filename(beat.filename):
                    beatFileName = secure_filename(beat.filename)
                    beatFilePath = path.join(current_app.config['TEMP_DIR'], beatFileName)
                    beat.save(beatFilePath)
                    
                    is_duplicate, beat_hash = check_beat_duplicate(beatFilePath)
                    if not is_duplicate:
                        beatInfo = request.form

                        beatName = beatInfo['name']
                        beatcategory = beatInfo['category']
                        beatLeasePrice = beatInfo['leasePrice']
                        beatSellingPrice = beatInfo['sellingPrice']

                        beatFilePath = save_beat_permanently(beatFileName)

                        # crop a 30 seconds preview of the beat
                        crop_beat(beatFilePath)

                        # Get metadata from the audio file using ffmpeg
                        run(main(beatFilePath))
                        
                        if preview is None:
                            return make_response({'status': 0, 'message':  'Could not upload beat successfully.'})

                        insertBeatQuery = '''INSERT INTO beat (beat_id, producer_id, name, category, beat_file, lease_price, 
                        selling_price, beat_hash) VALUES (UUID_TO_BIN(UUID()), UUID_TO_BIN('{}'), '{}', '{}', '{}', '{}', {}, {}, '{}')
                        '''.format(user_info['sub'], beatName, beatcategory, beatFileName, beatLeasePrice, beatSellingPrice, 
                            beat_hash)

                        databaseConnection = db.get_db()
                        databaseCursor = databaseConnection.cursor()

                        result = databaseCursor.execute(insertBeatQuery)
                        databaseConnection.commit()

                        if result is not None:
                            return make_response({'status': 1, 'message': 'The beat has been successfully uploaded'}, 200)
                        else:
                            return make_response({'status': 0, 'message': 'An error occurred when uploading the beat'}, 500)
                    else:
                        return make_response({'status': 0, 'message': 'Duplicate file upload.'}, 409)
                else:
                    return make_response({'status': 0, 'message': 'File type not allowed.'}, 409)
            else:
                return make_response({'status': 0, 'message': 'No beat file uploaded'}, 400)
        else:
            return make_response({'status': 0, 'message': 'Must be logged in to perform this request.'}, 404)
    else:
        return make_response({'status': 0, 'message': 'Bad Request'}, 400)


@bp.route('beat/delete', methods=['POST'])
def delete_beat():
    ''' remove the beat with beat_id from the database'''
    if request.content_type is 'application/json':
        token = request.headers.get('Authorization').split(' ')[1]
        if is_logged_in(token): 
            beat_details = beat_exists()
            if beat_details[0]:
                # remove the beat entry from the database
                cur = get_db().cursor()
                query = "DELETE FROM beat WHERE beat_id={} LIMIT 1"
                result = cur.execute(query)
                cur.commit()

                # remove the beat's file from the filesystem
                try:
                    Path.unlink(beat_details[1])
                except FileNotFoundError as e:
                    log_error("At unlink request file, " + str(e), "fnf_error_logs.txt")
                    return make_response({'status': 0,
                                          'message': 'Beat does not exist or has\
                                                      already been deleted.'}
                                          , 404)
                if result == 1:
                    response = make_response({'status':1, 'message': 'Successfully deleted beat'})
                    return resp
                else:
                    resp = make_response({'status':0, 'message': 'Error occurred when deleting the beat'}, 404)
                    return resp
            else:
                return make_response({'status':0, 'message': 'Beat does not exists or has been deleted.'} , 404)
        else:
            return make_response({'status': 0, 'message': 'Must be logged in to complete this request.'}, 404)
    else:
        return make_response({'status':0, 'message': 'Invalid content type.'}, 404)


@bp.route('fetch/all', methods=['GET'])
def fetch_beats():
    request_info = request.get_json()
    limit = request.args.get('limit', 30)
    skip = request.args.get('skip', 0)

    # fetch all beats
    beats = get_beats(limit, skip)
    if not beats:
        return make_response({'status': 0, 'message': 'No beats found'}, 200)
    # return the beats
    return make_response({'status': 1, 'message': 'Beats fetched successfully','beats': beats}, 200)


@bp.route('<beat_id>', methods=['GET'])
def fetch_beat(beat_id):
    query = '''SELECT (BIN_TO_UUID(beat.beat_id)) beat_id, beat.name, beat.category, beat.beat_file, beat.lease_price, 
    beat.selling_price, beat.upload_date, (BIN_TO_UUID(producer.producer_id)) producer_id, producer.profile_image, producer.name producer FROM beat INNER JOIN producer ON 
    beat.producer_id=producer.producer_id WHERE beat.beat_id = UUID_TO_BIN("{}")'''.format(escape(beat_id))

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute(query) 
    beat = cur.fetchone()

    if not beat:
        return render_template('beat.html'), 404

    crumbs = [
        {"name": "Discover", "url": url_for('routes.discover')},
        {"name": beat["category"], "url": url_for('category.category', category='_'.join(beat["category"].lower().split(' ')))}
    ]
    return render_template('beat.html', page=beat["name"], crumbs=crumbs, beat=beat), 200


def get_beats(limit, skip):
    ''' This function returns beats made by a certain producer,
    if passed to the function, and adds a limit and offset contraint
    to the query'''
    conn = db.get_db()
    cur = conn.cursor()
    query = '''SELECT (BIN_TO_UUID(beat.beat_id)) beat_id, beat.name, beat.category, beat.beat_file, beat.lease_price, 
    beat.selling_price, beat.upload_date, producer.name producer FROM beat INNER JOIN producer ON 
    beat.producer_id=producer.producer_id'''
    # if producer is not None:
    #     query = str.join(' ', [query, 'WHERE producer_id={}'.format(producer)])

    query = str.join(' ', [query, 'LIMIT {},{}'.format(skip, limit)])

    cur.execute(query)
    conn.commit()
    res = cur.fetchall()
    return res

def beat_exists(beat_id):
    ''' Function to check whether a beat is in the database and that it exists in the file
        system'''
    cur = db.get_db().cursor()
    query = "SELECT address FROM beat WHERE beat_id={} LIMIT 1".format(beat_id)
    cur.execute(query)

    result = cur.fetch_one()
    if result is not None and path.exists(result['address']):
        return True, result['address']

    return False, None

def check_beat_duplicate(beatFilePath):
    ''' Queries database for the beat hash and
    returns True if the hash exists, False otherwise
    '''
    with open(beatFilePath, "rb") as f:
        try:
            beat_hash = md5(f.read()).hexdigest()
            check_duplicate_beat = "SELECT beat_hash FROM beat WHERE beat_hash = '%s'" % beat_hash
            cur = db.get_db().cursor()
            return (cur.execute(check_duplicate_beat) > 0), beat_hash
        except OSError as e:
            log_error("At check_beat_duplicate, " + str(e), "os_error_logs.txt")

def save_beat_permanently(beatFilePath):
    '''
    Saves the temporary file at beatFilePath to the BEAT_DIR
    then deletes the temporary file
    '''
    with open(filename, "rb") as f:
        try:
            file_path = path.join(current_app.config['BEAT_DIR'], filename)
            beatFile = open(file_path, "wb")
            beatFile.write(f.read())
            beatFile.close()
            f.close()
            return file_path
        except OSError as e:
            log_error("At save_beat_permanently, " + str(e), "os_error_logs.txt")