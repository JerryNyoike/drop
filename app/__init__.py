from os import path, makedirs
import pymysql
from . import routes, user, auth, db, beat
from flask import Flask, current_app
from datetime import datetime
from .helpers import log_error
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        ALLOWED_EXTENSIONS=['mp3', 'flac', 'ogg', 'wav', 'm4a']
    )
    app.config.from_pyfile("../config.py", silent=True)

    with app.app_context():
        # Set the secret key to some random bytes. Keep this really secret!
        app.secret_key = current_app.config['SCRT']

        try:
            if not path.exists(current_app.instance_path):
                makedirs(app.instance_path)

            if not path.exists(current_app.config['BEAT_DIR']):
                makedirs(current_app.config['BEAT_DIR'])

            if not path.exists(current_app.config['PREVIEW_DIR']):
                makedirs(current_app.config['PREVIEW_DIR'])

            if not path.exists(current_app.config['TEMP_DIR']):
                makedirs(current_app.config['TEMP_DIR'])

            if not path.exists(current_app.config['LOG_DIR']):
                makedirs(current_app.config['LOG_DIR'])

        except OSError as e:
            log_error("At create_app, " + str(e), "os_error_logs.txt")

    db.init_app(app)

    app.register_blueprint(routes.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(beat.bp)

    CORS(app)

    return app
