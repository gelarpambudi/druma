import os
import sys
import urllib.request
import pandas as pd
import numpy as np
import cv2 as cv
import threading
import requests
import json
import time

from flask import request, render_template, session, redirect, flash
from werkzeug.utils import secure_filename
from app import app
from image_processing import *
from req import *


@app.route("/", methods=['GET','POST'])
def home():
    if request.method == "POST":
        start = time.time()
        if 'files' not in request.files:
            flash(u'No file part')
            return redirect(request.url)

        file = request.files['files']
        
        if file and allowed_file(file.filename):
            img_path = save_image(file)
            input_img = {'image': open(img_path, 'rb')}

            #multithread request
            threads = [api_request(input_img, url) for url in URL]
            #start thread
            for thread in threads:
                thread.start()
            #stop thread
            for thread in threads:
                thread.join()
            
            detected_lines = threads[0].result
            boxes = threads[1].result

            res_image = load_image_as_np(img_path)

            for i in range(0, len(detected_lines)):
                rho = detected_lines[i][0][0]
                theta = detected_lines[i][0][1]
                draw_line(res_image, rho, theta)
            
            for box in boxes[['xmin', 'ymin', 'xmax', 'ymax']].values:
                draw_box(res_image, box, [255,130,0], 3)
            
            final_img = save_np_image(res_image, file.filename)
            img_file_path = os.path.join('uploads/', final_img)

            print("Execution time: ", time.time()-start)

            return render_template("index.html", img_path=img_file_path, filename=final_img)
        else:
            flash(u'Allowed image types are -> png, jpg, jpeg, tif')
            return redirect(request.url)

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='7777')