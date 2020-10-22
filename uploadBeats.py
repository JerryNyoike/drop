import requests
import random
import os
from functools import partial

uploadUrl = 'http://127.0.0.1/producer/upload'
headers = { 'Authorization': 'Bearer ' }



def upload(beatDir, beat):
    def beat_category(beat_name):
        return beat_name.split('.')[0]

    beatPath = os.path.join(beatDir, beat)
    files = {'file': open(beatPath, 'rb')}
    payload = {
            'name': beat,
            'category': beat_category(name),
            'leasePrice': random.randrange(200, 300),
            'sellingPrice': random.randrange(500, 1000)
            }
    resp = requests.post(uploadUrl, files=files, data=payload, headers = headers)
    return resp.status_code


def uploadBeats(beat_directory_path):
    def upload_all(beat_folder, upload_func):
        upload_part = partial(upload, beat_directory_path)
        folder_path = os.path.join(root_path, beat_folder)
        beat_list = os.list_dir(folder_path)
        return list(map(upload_part, beat_list))
        
    beat_folders = os.listdir(beat_directory_path)
    return list(map(upload_all, beat_folders))

uploadBeats(os.path.join(os.getcwd(), "app", "GTZAN", "genres_original"))
