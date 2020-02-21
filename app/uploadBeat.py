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
