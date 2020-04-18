from os import path, makedirs
import pymysql
from . import auth, db, beat
from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        ALLOWED_EXTENSIONS=['mp3', 'flac', 'ogg', 'wav', 'm4a']
    )
    app.config.from_pyfile("../config.py", silent=True)

    try:
    
    except OSError as e:
    print(e)
    try:
        if not path.exists(beat_path):
            makedirs(app.instance_path)

        if not path.exists(current_app.config['BEAT_DIR']):
            makedirs(current_app.config['BEAT_DIR'])

        if not path.exists(current_app.config['PREVIEW_DIR']):
            makedirs(current_app.config['PREVIEW_DIR'])

        if not path.exists(current_app.config['TEMP_FOLDER']):
            makedirs(current_app.config['TEMP_FOLDER'])

    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(beat.bp)

    CORS(app)

    return app
