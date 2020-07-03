import os
import math
import cv2
import numpy as np
from PIL import Image, ImageEnhance

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def recogLp(filename):
    path = './base/' + filename
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img_h, img_w = img.shape[:2]
    org_img = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # color gray
    img = cv2.bilateralFilter(img, 9, 75, 75) # blur filter
    img = cv2.Canny(img, 50, 50) # extract edge

    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # objects list
    
    rec_box = []; points = []; 
    f_count = 0; select = 0; 
    for i in range(len(contours)):
        x, y, w, h = cv2. boundingRect(contours[i])
        area = w*h; ratio = float(w)/h;
        # filtering box size << overfitted
        if ratio >= 0.3 and ratio < 1.0 and area >= 2000 and area <= 5000: 
            # print("x: ", x, " y: ", y, " w: ", w, " h: ", h)
            points.append((x, y, w, h)) # points[]
            # print("ratio: ", ratio, " area: ", area)
            # cv2.rectangle(org_img, (x, y), (x+w, y+h), (0, 225, 0), 1)
            rec_box.append(cv2.boundingRect(contours[i]))
    
    for i in range(len(rec_box)):
        for j in range(len(rec_box)-(i+1)):
            if rec_box[j][0] > rec_box[j+1][0]:
                tmp = rec_box[j]
                rec_box[j] = rec_box[j+1]
                rec_box[j+1] = tmp

    for m in range(len(rec_box)):
        count = 0
        for n in range(m+1, len(rec_box)-1):
            delta_x = abs(rec_box[n+1][0]-rec_box[m][0])
            if delta_x > 150: break;
            delta_y = abs(rec_box[n+1][1]-rec_box[m][1])
            if delta_x == 0: delta_x = 1
            if delta_y == 0: delta_y = 1
            gradient = float(delta_y)/float(delta_x)
            if gradient < 0.25: count += 1
        if count > f_count:
            f_count = count; select = m

    first_p_box = points[0]
    last_p_box = points[len(points)-1]

    a = abs(last_p_box[0]+last_p_box[2] - first_p_box[0])
    b = abs(last_p_box[1] - first_p_box[1])
    plate_w = math.sqrt(a**2 + b**2)

    p1 = np.float32([
        [first_p_box[0], first_p_box[1]], 
        [last_p_box[0]+last_p_box[2], last_p_box[1]], 
        [first_p_box[0], first_p_box[1]+first_p_box[3]],
        [last_p_box[0]+last_p_box[2], last_p_box[1]+last_p_box[3]]
    ])
    p2 = np.float32([
        [first_p_box[0], first_p_box[1]], 
        [first_p_box[0]+plate_w, first_p_box[1]], 
        [first_p_box[0], first_p_box[1]+first_p_box[3]],
        [first_p_box[0]+plate_w, first_p_box[1]+first_p_box[3]]
    ])
    org_img = cv2.warpPerspective(org_img, cv2.getPerspectiveTransform(p1, p2), (img_w, img_h))
    
    print(rec_box[select])
    org_img=org_img[rec_box[select][1]-20:rec_box[select][3]+rec_box[select][1]+20,rec_box[select][0]-100:rec_box[select][0]+100] 
    rslt_detect = cv2.resize(org_img, None,fx=1.8,fy=1.8,interpolation=cv2.INTER_CUBIC+cv2.INTER_LINEAR)
    cv2.imshow('test', rslt_detect)
    cv2.waitKey(0)

    img_recog = cv2.cvtColor(rslt_detect, cv2.COLOR_BGR2GRAY)
    img_recog = cv2.morphologyEx(img_recog, cv2.MORPH_CLOSE, kernel=np.ones((3,3), np.uint8))
    _, img_recog = cv2.threshold(img_recog, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite('./rslt_detect/thres_'+filename, img_recog)
    rslt_recog = pytesseract.image_to_string(img_recog, lang='kor_lp_gen', config='--psm 7 --oem 2')

    return rslt_recog

filenames = os.listdir('./base')
for filename in filenames:
    print(recogLp(filename))