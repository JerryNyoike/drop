from os import path, makedirs, sep
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
import librosa
import pandas as pd
import numpy as np
import os
import pathlib
import csv
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import joblib


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
    extension = beat_path.split('.')[-1]
    preview_name = beat_path.split(sep)[-1]
    if extension in current_app.config['ALLOWED_EXTENSIONS']:
        beat = AudioSegment.from_file(beat_path, format=extension)

        # slice the audio to the first 30 seconds
        preview = beat[:30000]

        # save preview to the file system
        filename = path.join(current_app.config['PREVIEW_DIR'], preview_name)

        preview.export(filename, format='mp3')

        return filename
    
    return None

def extract_features(beat_path):
    filename = beat_path.split('/')[-1]
    # genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
    y, sr = librosa.load(beat_path, mono=True, duration=30)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    tempo = librosa.beat.tempo(y=y)
    data = [ 
        np.mean(chroma_stft), np.mean(rmse), np.mean(spec_cent), np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), tempo[0] 
    ]  
    for e in mfcc:
        data.append(np.mean(e))

    return (filename, data)
            

@bp.route('upload', methods=['POST'])
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

                        beatFilePath = save_beat_permanently(beatFilePath)

                        # crop a 30 seconds preview of the beat
                        preview_path = crop_beat(beatFilePath)

                        file, features = extract_features(preview_path)
                        features = np.asarray([features])
                        print(features.shape)
                        
                        scaler = StandardScaler()
                        X = scaler.fit_transform(np.array(features, dtype = float))

                        model = load_model('app/model/cnn')
                        # forest = joblib.load("app/model/forest")
                        prediction = model.predict(X)

                        genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
                        print("---RESULTS---")
                        print(prediction)
                        predicted_genre = genres[np.argmax(prediction[0])]
                        print("Predicted: " + predicted_genre)

                        # extract features from the beat preview
                        # extract_features(preview_path)

                        # Get metadata from the audio file using ffmpeg
                        # run(main(beatFilePath))
                        
                        if preview_path is None:
                            return make_response({'status': 0, 'message':  'Could not upload beat successfully.'})

                        insertBeatQuery = '''INSERT INTO beat (beat_id, producer_id, name, category, beat_file, lease_price, 
                        selling_price, beat_hash) VALUES (UUID_TO_BIN(UUID()), UUID_TO_BIN('{}'), '{}', '{}', '{}', {}, {}, '{}')
                        '''.format(user_info['sub'], beatName, beatcategory, beatFileName, beatLeasePrice, beatSellingPrice, 
                            beat_hash)

                        databaseConnection = db.get_db()
                        databaseCursor = databaseConnection.cursor()

                        result = databaseCursor.execute(insertBeatQuery)
                        databaseConnection.commit()

                        if result is not None:
                            return render_template('dashboard/upload.html', page="Upload Beat", success="Beat Uploaded"), 200
                        else:
                            return render_template('dashboard/upload.html', page="Upload Beat", error="Something went wrong"), 500
                    else:
                        return render_template('dashboard/upload.html', page="Upload Beat", error="Duplicate file upload."), 500
                else:
                    return render_template('dashboard/upload.html', page="Upload Beat", error="File type not allowed."), 409
            else:
                return render_template('dashboard/upload.html', page="Upload Beat", error="No beat file uploaded"), 400
        else:
            return render_template('dashboard/upload.html', page="Upload Beat", error="Must be logged in to upload beat."), 403
    else:
        return render_template('dashboard/upload.html', page="Upload Beat", error="Bad Request"), 400


@bp.route('beat/delete', methods=['DELETE'])
def delete_beat():
    ''' remove the beat with beat_id from the database'''
    if request.content_type == 'application/json':
        token = request.cookies.get('token')
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
            return redirect(url_for('client.login'), 401)
    else:
        return make_response({'status':0, 'message': 'Invalid content type.'}, 404)


@bp.route('interaction', methods=['POST'])
def createInteraction():
    def recordInteraction(beat_id):
        conn = db.get_db()
        cur = conn.cursor()
        query = '''INSERT INTO beat_interaction (interaction_id, beat_id) VALUES (UUID_TO_BIN(UUID()), UUID_TO_BIN("{}"))'''.format(beat_id)
        
        result = cur.execute(query)
        cur.commit()
        return result

    requestInfo = request.get_json()
    userInfo = is_logged_in(request.cookies.get('token'))
    if userInfo is not None and userInfo['typ'] == 'client':
        if recordInteraction(beat_id) == 1:
            return make_response({"status": 1, "message": "Successful request"}, 200)
        else:
            return make_response({"status": 1, "message": "Request not successful"}, 200)
    else:
        return make_response({"status": 1, "message": "Unauthorized"}, 403)


@bp.route('interactions/max', methods=['GET'])
def getBeatWithMaxInteractions():
    conn = db.get_db()
    cur = conn.cursor()
    def interactions(beat):
        query = '''SELECT interaction_time FROM beat_interaction WHERE  TIMESTAMPDIFF(DAY, CURRENT_TIMESTAMP, interaction_time)=5 AND beat_id=UUID_TO_BIN("{}")'''.format(beat['beat_id'])
        result = cur.execute(query)
        conn.commit()
        return beat['beat_id'], result

    def getProducerUploads(producer):
        query = '''SELECT beat_id, name FROM beats WHERE producer_id=UUID_TO_BIN("{}")'''.format(producer)
        cur.execute(query)
        conn.commit()
        return cur.fetchall()

    requestInfo = request.get_json()
    userInfo = is_logged_in(request.cookies.get('token'))

    uploads = getProducerUploads(userInfo['sub'])
    uploadInteractions = list(map(interactions, uploads))

    if userInfo is not None and userInfo['typ'] == 'producer':
        return make_response({"status": 1, "message": "Request successful", "data": uploadInteractions}, 200)
    else:
        return make_response({"status": 1, "message": "Unauthorized"}, 403)


@bp.route('fetch/all', methods=['GET'])
def fetch_beats():
    request_info = request.get_json()
    limit = request.args.get('limit', 30)
    skip = request.args.get('skip', 0)

    # fetch all beats
    beats = get_beats(limit, skip)
    if not beats:
        return make_response({'status': 0, 'message': 'No beats found'}, 404)
    # return the beats

    return make_response({'status': 1, 'message': 'Beats fetched successfully', 'beats': beats}, 200)


@bp.route('fetch/new', methods=['GET'])
def fetch_new():
    request_info = request.get_json()
    limit = request.args.get('limit', 30)
    skip = request.args.get('skip', 0)

    # fetch latest beats
    query = '''SELECT (BIN_TO_UUID(beat.beat_id)) beat_id, beat.name, beat.beat_file, beat.lease_price, 
    beat.selling_price, beat.upload_date, beat.category, BIN_TO_UUID(producer.producer_id) producer_id, producer.name producer FROM 
    beat INNER JOIN producer ON beat.producer_id=producer.producer_id LEFT JOIN beat_category ON 
    beat.beat_id=beat_category.beat_id LIMIT {} ORDER BY beat.upload_date DESC'''.format(limit)

    cur = db.get_db().cursor()
    cur.execute(query) 
    beats = cur.fetchone()

    if not beats:
        return make_response({'status': 0, 'message': 'No beats found'}, 404)
    
    # return the beats
    return make_response({'status': 1, 'message': 'Beats fetched successfully', 'beats': beats}, 200)


@bp.route('fetch/in', methods=['GET'])
def fetch_in():
    request_info = request.get_json()

    if not request_info:
        return make_response({'status': 0, 'message': 'Missing request body'}, 400)

    make_bin_id = lambda uuid : "UUID_TO_BIN('" + uuid + "')"
    beat_ids = list(map(make_bin_id, request_info.beat_ids))

    # fetch beats with above ids
    query = '''SELECT (BIN_TO_UUID(beat.beat_id)) beat_id, beat.name, beat.beat_file, beat.lease_price, 
    beat.selling_price, beat.upload_date, beat.category, BIN_TO_UUID(producer.producer_id) producer_id, producer.name producer FROM 
    beat INNER JOIN producer ON beat.producer_id=producer.producer_id LEFT JOIN beat_category ON 
    beat.beat_id=beat_category.beat_id WHERE beat.beat_id IN ({})'''.format(','.join(beat_ids))

    cur = db.get_db().cursor()
    cur.execute(query) 
    beats = cur.fetchone()

    if not beats:
        return make_response({'status': 0, 'message': 'No beats found'}, 404)
    
    # return the beats
    return make_response({'status': 1, 'message': 'Beats fetched successfully', 'beats': beats}, 200)


@bp.route('fetch/recent', methods=['GET'])
def fetchRecent():
    request_info = request.get_json()

    # fetch all beats
    query = '''SELECT (BIN_TO_UUID(beat.beat_id)) beat_id, beat.name, beat.beat_file, beat.lease_price, 
    beat.selling_price, beat.upload_date, beat.category, BIN_TO_UUID(producer.producer_id) producer_id, producer.name producer FROM 
    beat INNER JOIN producer ON beat.producer_id=producer.producer_id ORDER BY beat.upload_date DESC LIMIT {}'''.format(15)

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute(query)
    beats = cur.fetchall()
    if not beats:
        return make_response({'status': 0, 'message': 'No beats found'}, 404)
    # return the beats

    return make_response({'status': 1, 'message': 'Beats fetched successfully', 'beats': beats}, 200)

@bp.route('producer', methods=['GET'])
def fetchProducerBeats(producer_id):
    producer_info = is_logged_in(request.cookies.get('token'))

    if producer_info is not None and producer_info['typ'] == 'producer':
        query = '''SELECT (BIN_TO_UUID(beat.beat_id)) beat_id, beat.name, beat.category, beat.beat_file, beat.lease_price, beat.selling_price, beat.upload_date, beat.category, (BIN_TO_UUID(producer.producer_id)) producer_id, producer.profile_image, producer.name producer FROM beat INNER JOIN producer ON beat.producer_id=producer.producer_id WHERE producer.producer_id = UUID_TO_BIN("{}")'''.format(escape(producer_id))

        conn = db.get_db()
        cur = conn.cursor()
        cur.execute(query)
        beats = cur.fetchall()

        if len(beats) > 0:
            return make_response({'status': 1, 'message': 'Beats fetched successfully', 'beats': beats}, 200)
        else:
            return make_response({'status': 0, 'message': 'No beats found'}, 404)
    else:
        return redirect(url_for('producer.login'), 401)


@bp.route('<beat_id>', methods=['GET'])
def fetch_beat(beat_id):
    query = '''SELECT (BIN_TO_UUID(beat.beat_id)) beat_id, beat.name, beat.category, beat.beat_file, beat.lease_price, 
    beat.selling_price, beat.upload_date, beat.category, (BIN_TO_UUID(producer.producer_id)) producer_id, producer.profile_image, producer.name producer FROM beat INNER JOIN producer ON 
    beat.producer_id=producer.producer_id WHERE beat.beat_id = UUID_TO_BIN("{}")'''.format(escape(beat_id))

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute(query) 
    beat = cur.fetchone()

    if not beat:
        return render_template('beat.html'), 404

    crumbs = [
        {"name": "Discover", "url": url_for('routes.discover'), "active": "true"},
        {"name": beat["category"], "url": url_for('category.category', category='_'.join(beat["category"].lower().split(' ')))}
    ]
    return render_template('beat.html', page=beat["name"], crumbs=crumbs, beat=beat), 200


def get_beats(limit, skip):
    ''' This function returns beats made by a certain producer,
    if passed to the function, and adds a limit and offset contraint
    to the query'''
    conn = db.get_db()
    cur = conn.cursor()
    query = '''SELECT (BIN_TO_UUID(beat.beat_id)) beat_id, beat.name, beat.beat_file, beat.lease_price, 
    beat.selling_price, beat.upload_date, beat.category, BIN_TO_UUID(producer.producer_id) producer_id, producer.name producer FROM 
    beat INNER JOIN producer ON beat.producer_id=producer.producer_id LIMIT {}'''.format(limit)

    cur.execute(query)
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
    with open(beatFilePath, "rb") as f:
        try:
            file_path = path.join(current_app.config['BEAT_DIR'], beatFilePath.split(sep)[-1])
            beatFile = open(file_path, "wb")
            beatFile.write(f.read())
            beatFile.close()
            f.close()
            return file_path
        except OSError as e:
            log_error("At save_beat_permanently, " + str(e), "os_error_logs.txt")
