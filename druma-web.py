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
import concurrent

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
            #input_img = {'image': open(img_path, 'rb')}
            

            
            #multithread request
            threads = [api_request(img_path, url) for url in URL]
            #start thread
            for thread in threads:
                thread.start()
            #stop thread
            for thread in threads:
                thread.join()
            
            detected_lines = threads[1].result
            boxes = threads[0].result
            
            res_image = load_image_as_np(img_path)

           
            a = []
            b = []

            if detected_lines is not None and boxes is not None:
                for i in range(0, len(detected_lines)):
                    rho = detected_lines[i][0][0]
                    theta = detected_lines[i][0][1]
                    res = draw_line(res_image, rho, theta)
                    a.append(res[0])
                    b.append(res[1])

                line_start = np.asarray(a, dtype=np.float32)
                line_end = np.asarray(b, dtype=np.float32)
                center_point = boxes[['xcenter','ycenter']].to_numpy()
            
                boxes['color'] = get_box_color(center_point, line_start, line_end)
                for box in boxes[['xmin', 'ymin', 'xmax', 'ymax', 'color']].values:
                    if box[-1] == 'red':
                        draw_box(res_image, box[:4], [0,0,255], 2)
                    elif box[-1] == 'yellow':
                        draw_box(res_image, box[:4], [0,255,255], 2)
                    elif box[-1] == 'green':
                        draw_box(res_image, box[:4], [0,255,0], 2)

            elif detected_lines is None and boxes is not None:
                for box in boxes[['xmin', 'ymin', 'xmax', 'ymax']].values:
                    draw_box(res_image, box, [0,255,0], 2)

            elif detected_lines is not None and boxes is None:
                for i in range(0, len(detected_lines)):
                    rho = detected_lines[i][0][0]
                    theta = detected_lines[i][0][1]
                    res = draw_line(res_image, rho, theta)
            else:
                pass
            
            final_img = save_res_image(res_image, file.filename)
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