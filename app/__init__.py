import os
import pymysql
from . import auth, db, uploadBeat
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DB='dropbeats'
        , DB_HOST='localhost'
        , DB_USER='droppy'
        , DB_PASS='dropitlikeitshot'
        , CURSOR=pymysql.cursors.DictCursor
        , SCRT='topsecrettochangelater')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(uploadBeat.bp)

    return app
