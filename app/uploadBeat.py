#pip install flask-mysql
import pymysql
from flask import Flask, make_response, request

from . import db

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'penguin'
app.config['MYSQL_PASSWORD'] = 'penguin'
app.config['MYSQL_DB'] = 'MULTIMEDIA'
app.config['MYSQL_CURSOR'] = pymysql.cursors.DictCursor

@app.route('/')
def index():
    return 'This is the default homepage'

@app.route('/redirectURL', methods=['POST'])
def insertBeat():
    #Check for JSON
    if request.is_json():
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

        return "The beat has been successfully uploaded"

    else:
        return make_response({'status': 0, 'message': 'Invalid data.'}, 400)



if __name__ == '__main':
    app.run(debug=True)
