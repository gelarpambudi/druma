import requests
import json
import pandas as pd
import numpy as np
from threading import Thread

ALLOWED_EXTENSIONS = set(['tiff', 'tif', 'jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG', 'TIF', 'TIFF'])
URL = ['http://192.168.88.7:5555/api/hough-transform',
        'http://192.168.88.7:5555/api/predict-deepforest']


class api_request(Thread):
    
    def __init__ (self, input_image, url):
        self.result = None
        self.input_image = input_image
        self.url = url
        super(api_request, self).__init__()

    def run(self):
        if self.url == URL[0]:
            r = requests.post(self.url, params={"image": self.input_image})
            data = json.dumps(r.json())
            self.result = np.array(json.loads(data)["lines"])
        elif self.url == URL[1]:
            r = requests.post(self.url, params={"image": self.input_image})
            data = json.dumps(r.json())
            self.result = pd.read_json(data, orient='index')


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''   
def post_req_deepforest(url, input_image):
    r = requests.post(url, params={"image": input_image})
    data = json.dumps(r.json())
    return pd.read_json(data, orient='index')

def post_req_hough(url, input_image):
    r = requests.post(url, params={"image": input_image})
    data = json.dumps(r.json())
    return np.array(json.loads(data)["lines"])
'''

