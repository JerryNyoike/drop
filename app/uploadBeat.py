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
            if beat_exists():
                #logic here
                cur = get_db().cursor()
                query = "DELETE FROM beat WHERE beat_id={} LIMIT 1"
                result = cur.execute(query)
                cur.commit()
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


def beat_exists(beat_id):
    cur = get_db().cursor()
    query = "SELECT name FROM beat WHERE beat_id={} LIMIT 1".format(beat_id)
    cur.execute(query)

    result = cur.fetch_one()
    if result is not None:
        return True

    return False
