import numpy as np
import pandas as pd
import cv2 as cv
import os
from PIL import Image
from werkzeug.utils import secure_filename
from app import app

def load_image_as_np(img_file):
    img = Image.open(img_file)
    return np.array(img)

def save_image(img_file):
    filename = secure_filename(img_file.filename)
    img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

def save_np_image(np_image, filename):
    cv.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'result-'+filename), np_image)
    return 'result-' + filename 

def draw_line(image, rho, theta):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1 = (int(x0 + 2000*(-b)), int(y0 + 2000*(a)))
    pt2 = (int(x0 - 2000*(-b)), int(y0 - 2000*(a)))
    cv.line(image, pt1, pt2, (255,255,0), 3, cv.LINE_AA)

def draw_box(image, box, color, thickness=1):
    b = np.array(box).astype(int)
    cv.rectangle(image, (b[0], b[1]), (b[2], b[3]), color, thickness, cv.LINE_AA)
