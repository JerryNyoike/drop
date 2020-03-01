import pymysql
from flask import Blueprint, make_response, request, current_app

from . import db
from .auth import is_logged_in


bp = Blueprint('uploadBeat', __name__, url_prefix="/beat")


@bp.route('/upload', methods=['POST'])
def insertBeat():
    #Check for JSON
    if request.is_json():
        producer = request['token']
        if is_logged_in(producer):
            if request.files['beat'] is not None:
                beatInfo = request.get_json()

                producerID = beatInfo['producerID']
                beatName = beatInfo['name']
                beatGenre = beatInfo['genre']
                beatFilePath = beatInfo['filePath']
                beatLeasePrice = beatInfo['leasePrice']
                beatSellingPrice = beatInfo['sellingPrice']

                insertBeatQuery = "INSERT INTO beat VALUES ({}, {}, {}, {}, {}, {}, {}".format(producerID, beatName, beatGenre, beatFilePath, beatLeasePrice, beatSellingPrice)

                databaseConnection = db.get_db()
                databaseCursor = databaseConnection.cursor()

                databaseCursor.execute(insertBeatQuery)
                databaseConnection.commit()

                return make_response({'status': 1, 'message': "The beat has been successfully uploaded"}, 200)
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
                except FileNotFoundError e:
                    return make_response({'status': 0,
                                          'message': 'Beat does not exist or has
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


@bp.route('/fetch/all', method=['GET'])
def fetch_beats():
    if request.content_type is 'application/json':
        request_info = request.get_json()
        limit = request.args.get('limit', 30)
        skip = request.args.get('skip', 0)
        # check that user is logged in
        user = is_logged_in(request_info['tkn'])
        if user is not False:
            # check the user type
            if user['typ'] is 'producer':
                # fetch only beats uploaded by the producer
                beats = get_beats(user['aud'], limit, skip)
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
            return make_response({'status': 0, 'message': 
                                'Must be logged in to complete this request'}, 403)
        
    else:
        return make_response({'status': 0, 'message': 'Invalid content type.'}, 404)


def get_beats(producer=None, limit, skip):
    ''' This function returns beats made by a certain producer,
    if passed to the function, and adds a limit and offset contraint
    to the query'''
    cur = get_db().cursor()
    query = 'SELECT * FROM beat'
    if producer is not None:
        query = str.join(' ', [query, 'WHERE producer_id={}'.format(producer)])

    query = str.join(' ', [query, 'LIMIT {},{}'.format(skip, limit)])

    cur.execute(query)
    cur.commit()
    return cur.fetch_all()

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
