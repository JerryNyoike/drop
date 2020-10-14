from os import path, makedirs, remove, sep
from pydub import AudioSegment
from pydub.utils import which
import pymysql
from flask import Blueprint, make_response, request, current_app
from werkzeug.utils import secure_filename
from hashlib import md5  
import librosa
import pandas as pd
import numpy as np
import os
import pathlib
import csv

from . import db
from .auth import is_logged_in


bp = Blueprint('beat', __name__, url_prefix="/beat")

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
    print(filename)
    header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
    header = header.split()
    for i in range(1, 21):
        header.append(f'mfcc{i}')

    with open('beat_data.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
        y, sr = librosa.load(beat_path, mono=True, duration=30)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        rmse = librosa.feature.rms(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        to_append = f'{filename} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'    
        for e in mfcc:
            to_append += f' {np.mean(e)}'

        print(to_append)
        file = open('beat_data.csv', 'a', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())

@bp.route('/upload', methods=['POST'])
def insertBeat():
    if request.content_type != 'multipart/form-data':
        token = request.headers.get('Authorization').split(' ')[1]
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
                        beatGenre = beatInfo['genre']
                        beatLeasePrice = beatInfo['leasePrice']
                        beatSellingPrice = beatInfo['sellingPrice']

                        beatFilePath = save_file_permanently(beatFilePath)
                        # crop a 30 seconds preview of the beat
                        preview = crop_beat(beatFilePath)

                        extract_features(preview)
                        
                        if preview is None:
                            return make_response({'status': 0, 'message':  'Could not upload beat successfully.'})

                        insertBeatQuery = '''INSERT INTO beat (beat_id, producer_id, name, genre, address, prev_address, lease_price, 
                        selling_price, beat_hash) VALUES (UUID_TO_BIN(UUID()), UUID_TO_BIN('{}'), '{}', '{}', '{}', '{}', {}, {}, '{}')
                        '''.format(user_info['sub'], beatName, beatGenre, beatFilePath, preview, beatLeasePrice, beatSellingPrice, 
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
        return make_response({'status': 0, 'message': 'Invalid data.'}, 400)


@bp.route('delete', methods=['POST'])
def delete_beat():
    ''' remove the beat with beat_id from the database'''
    if request.content_type == 'application/json':
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
        if user['typ'] == 'producer':
            # fetch only beats uploaded by the producer
            beats = get_beats(limit, skip, user['sub'])
            if beats is not None:
                # return the beats
                return make_response({'status': 1, 'message': 'Success.', 'data': beats}, 200)
            else:
                return make_response({'status': 0, 'message': 'No beats found.'}, 404)
        else:
            # fetch beats produced by all producers
            beats = get_beats(limit, skip)
            if beats is not None:   
                # return the beats
                return make_response({'status': 1, 'message': 'Success.', 'data': beats}, 200)
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
        beat_hash = md5(f.read()).hexdigest()
        check_duplicate_beat = "SELECT beat_hash FROM beat WHERE beat_hash = '%s'" % beat_hash
        cur = db.get_db().cursor()
        return (cur.execute(check_duplicate_beat) > 0), beat_hash

def save_file_permanently(beatFilePath):
    with open(beatFilePath, "rb") as f:
        file_path = path.join(current_app.config['BEAT_DIR'], beatFilePath.split(sep)[-1])
        beatFile = open(file_path, "wb")
        beatFile.write(f.read())
        beatFile.close()
        f.close()
        remove(beatFilePath)
        return file_path
