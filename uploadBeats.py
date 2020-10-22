import requests
import random
import os
from functools import partial

uploadUrl = 'http://127.0.0.1/producer/upload'
headers = { 'Authorization': 'Bearer ' }

def upload(beatDir, beat):
    def beat_category(beat_name):
        return beat_name.split('0')[0]

    beatPath = os.path.join(beatDir, beat)
    files = {'file': open(beatPath, 'rb')}
    payload = {
            'name': beat,
            'category': beat_category,
            'leasePrice': random.randrange(200, 300),
            'sellingPrice': random.randrange(500, 1000)
            }
    resp = requests.post(uploadUrl, files=files, data=payload, headers = headers)
    return resp.status_code


def uploadBeats(beat_directory_path):
    upload_part = partial(upload, beat_directory_path)
    responses = list()
    beat_list = os.listdir(beat_directory_path)[0:5]
    responses = list(map(upload_part, beat_list))

uploadBeats(os.path.join(os.getcwd(), "static", "test-beats"))
