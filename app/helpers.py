from hashlib import sha256
from os.path import join
from datetime import datetime
import jwt


def log_error(error, log_file):
    with open(join(".\\instance\\logs", log_file), "a") as f:
        f.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + error + "\n")
        f.close()

def is_logged_in(token):
    try:
        return jwt.decode(token, current_app.config['SCRT'], algorithm='HS256')
    except jwt.exceptions.DecodeError as e:
        log_error("At is_logged_in, " + str(e), "jwt_error_logs.txt")
        return make_response({'status': 0, 'message': 'Must be logged in to perform action'}, 401)

def string_hash(to_hash):
    return sha256(to_hash.encode()).hexdigest()