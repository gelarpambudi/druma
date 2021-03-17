import requests
import json
import pandas as pd
import numpy as np
from threading import Thread
from image_processing import save_image

ALLOWED_EXTENSIONS = set(['tiff', 'tif', 'jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG', 'TIF', 'TIFF'])
URL = [
        'http://deepforest.druma.com:5555/api/predict-deepforest',
        'http://hough.druma.com:4444/api/hough-transform'
        ]


class api_request(Thread):
    
    def __init__ (self, file, url, patch):
        self.result = None
        self.input_image = file
        self.url = url
        self.patch = patch
        super(api_request, self).__init__()

    def run(self):
        if self.url == URL[0]:
            r = requests.post(
                self.url,
                files={'image': open(self.input_image, 'rb')},
                data={'patch_size': self.patch}
                )
            data = json.dumps(r.json())
            self.result = pd.read_json(data, orient='index')
        elif self.url == URL[1]:
            r = requests.post(
                self.url,
                files={'image': open(self.input_image, 'rb')},
                data={'patch_size': self.patch}
                )
            data = json.dumps(r.json())
            #if data is not None and json.loads(data)["lines"] != "No Line Detected":
            #    self.result = np.array(json.loads(data)["lines"])
            self.result = pd.read_json(data, orient='index')

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

