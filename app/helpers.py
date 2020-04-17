from os.path import join
from datetime import datetime


def log_error(error, log_file):
    with open(join(".\\instance\\logs", log_file), "a") as f:
        f.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + error + "\n")
        f.close()