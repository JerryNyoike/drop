from os import path
from pydub import AudioSegment
import pymysql
from flask import Blueprint, make_response, request, current_app
from werkzeug.utils import secure_filename


from . import db
from .auth import is_logged_in


bp = Blueprint('beat', __name__, url_prefix="/beat")


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def crop_beat(beat_path):
    '''
    This function slices a beat to just the first 30
    seconds and saves the preview to the file system and
    database
    '''
    extension = beat_path.split('.')[1]
    preview_name = beat_path.split('/')[-1]
    if extension is in current_app['ALLOWED_EXTENSIONS']:
        if extension is 'mp3':
            beat = AudioSegment.from_mp3(beat_path)
        elif extension is 'ogg':
            beat = AudioSegment.from_ogg(beat_path)
        elif extension is 'flac':
            beat = AudioSegment.from_flac(beat_path)
        else:
            beat = AudioSegment.from_wav(beat_path)

    # slice the audio to the first 30 seconds
    preview = beat[:30000]

    # save preview to the file system and database
    filename = path.join(current_app['PREVIEW_DIR'], preview_name)
    preview.export(filepath)

    conn = db.get_db()
    cursor = conn.cursor()
    query = 'UPDATE beat SET prev_address = {} WHERE beat_id={}'.format(filepath, beat_id)
    result = cursor.execute(query)
    conn.commit()
        
    if result == 1:
        return True

    return False
        
@bp.route('/upload', methods=['POST'])
def insertBeat():
    if request.content_type != 'multipart/form-data':
        token = request.headers.get('Authorization').split(' ')[1]
        user_info = is_logged_in(token)
        if user_info is not False and user_info['typ'] == 'producer':
            if 'file' in request.files:
                    beat = request.files['file']
                    if beat.filename != '':
                        if beat and allowed_filename(beat.filename):
                            beatInfo = request.form

                            beatName = beatInfo['name']
                            beatGenre = beatInfo['genre']
                            beatFileName = secure_filename(beat.filename)
                            beatFilePath = path.join(current_app.config['UPLOAD_FOLDER'], beatFileName)
                            beat.save(beatFilePath)
                            beatLeasePrice = beatInfo['leasePrice']
                            beatSellingPrice = beatInfo['sellingPrice']
                            
                            insertBeatQuery = "INSERT INTO beat (beat_id, producer_id, name, genre, address, lease_price, selling_price) VALUES (UUID_TO_BIN(UUID()), UUID_TO_BIN('{}'), '{}', '{}', '{}', {}, {})".format(user_info['sub'], beatName, beatGenre, beatFilePath, beatLeasePrice, beatSellingPrice)

                            databaseConnection = db.get_db()
                            databaseCursor = databaseConnection.cursor()

                            result = databaseCursor.execute(insertBeatQuery)
                            databaseConnection.commit()

                            # crop a 30 seconds preview of the beat
                            crop_beat(beat_path)

                            if result is not None:
                                return make_response({'status': 1, 'message': 'The beat has been successfully uploaded'}, 200)
                            else:
                                return make_response({'status': 0, 'message': 'An error occurred when uploading the beat'}, 500)
                        else:
                            return make_response({'status': 0, 'message': 'Illegal file extension.'}, 400)
                    else:
                        return make_response({'status': 0, 'message': 'Upload file cannot be null'}, 400)
            else:
                return make_response({'status': 0, 'message': 'Upload file cannot be null.'}, 400)
        else:
            return make_response({'status': 0, 'message': 'Must be logged in to perform this request.'}, 404)
    else:
        return make_response({'status': 0, 'message': 'Invalid data.'}, 400)


@bp.route('delete', methods=['POST'])
def delete_beat():
    ''' remove the beat with beat_id from the database'''
    if request.content_type is 'application/json':
        if is_logged_in(request['tkn']):
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
                except FileNotFoundError:
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


@bp.route('/fetch/all', methods=['GET'])
def fetch_beats():
    token = request.headers.get('Authorization').split(' ')[1]
    request_info = request.get_json()
    user = is_logged_in(token)
    limit = request.args.get('limit', 30)
    skip = request.args.get('skip', 0)
    # check that user is logged in
    if user is not False:    
        # check the user type
        if user['typ'] is 'producer':
            # fetch only beats uploaded by the producer
            beats = get_beats(limit, skip, user['sub'])
            if beats is not None:
                # return the beats
                return make_response({'status': 1, 'message': 'Success.',
                    'data': beats}, 200)
            else:
                return make_response({'status': 0, 'message': 'No beats found.'}, 404)
        else:
            # fetch beats produced by all producers
            beats = get_beats(limit, skip)
            if beats is not None:   
                # return the beats
                return make_response({'status': 1, 'message': 'Success.',
                    'data': beats}, 200)
            else:
                return make_response({'status': 0, 'message': 'No beats found.'}, 404)   
    else:
        return make_response({'status': 0, 'message': 'Must be logged in to complete this request'}, 403)


def get_beats(limit, skip, producer=None):
    ''' This function returns beats made by a certain producer,
    if passed to the function, and adds a limit and offset contraint
    to the query'''
    conn = db.get_db()
    cur = conn.cursor()
    query = 'SELECT (BIN_TO_UUID(beat_id)) beat_id, address, genre, lease_price, selling_price, upload_date FROM beat'
    if producer is not None:
        query = str.join(' ', [query, 'WHERE producer_id={}'.format(producer)])

    query = str.join(' ', [query, 'LIMIT {},{}'.format(skip, limit)])

    cur.execute(query)
    conn.commit()
    res = cur.fetchall()
    print(res)
    return res

def beat_exists(beat_id):
    ''' Function to check whether a beat is in the database and that it exists in the file
        system'''
    cur = get_db().cursor()
    query = "SELECT address FROM beat WHERE beat_id={} LIMIT 1".format(beat_id)
    cur.execute(query)

    result = cur.fetch_one()
    if result is not None and Path.exists(result['address']):
        return True, result['address']

    return False, None