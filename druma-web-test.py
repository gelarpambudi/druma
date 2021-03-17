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
        patch_size = request.form['patch_size']
        spatial_resolution = request.form['spatial_resolution']
        
        if file and allowed_file(file.filename):
            img_path = save_image(file)
            
            threads = [api_request(img_path, url) for url in URL]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            
            detected_lines = threads[1].result
            boxes = threads[0].result
            
            res_image = load_image_as_np(img_path)


            if detected_lines is not None and boxes is not None:
                
                line_start = []
                line_end = []
                for index, row in detected_lines.iterrows():
                    cv.line(res_image,
                            (row["pt1"][0],row["pt1"][1]),
                            (row["pt2"][0],row["pt2"][1]),
                            color=[255,0,0],
                            thickness=1)
                    line_start.append(row["pt1"])
                    line_end.append(row["pt2"])

                line_start = np.asarray(line_start,dtype=np.float32)
                line_end = np.asarray(line_end,dtype=np.float32)
                center_point = boxes[['xcenter','ycenter']].to_numpy()
            
                boxes['color'] = get_box_color(center_point, line_start, line_end, spatial_resolution)
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
                for index, row in detected_lines.iterrows():
                    cv.line(res_image,
                            (row["pt1"][0],row["pt1"][1]),
                            (row["pt2"][0],row["pt2"][1]),
                            color=[255,0,0],
                            thickness=1)
            else:
                pass
            
            box_count = [
                0 if boxes[boxes.color == 'red'].shape[0] is None else boxes[boxes.color == 'red'].shape[0],
                0 if boxes[boxes.color == 'yellow'].shape[0] is None else boxes[boxes.color == 'yellow'].shape[0],
                0 if boxes[boxes.color == 'green'].shape[0] is None else boxes[boxes.color == 'green'].shape[0]
            ]
            final_img = save_res_image(res_image, file.filename)
            img_file_path = os.path.join('uploads/', final_img)

            print("Execution time: ", time.time()-start)

            return render_template("index.html", img_path=img_file_path, filename=final_img, box_count=box_count)
        else:
            flash(u'Allowed image types are -> png, jpg, jpeg, tif')
            return redirect(request.url)

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='7777')