import os
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
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(beat.bp)

    CORS(app)

    return app
