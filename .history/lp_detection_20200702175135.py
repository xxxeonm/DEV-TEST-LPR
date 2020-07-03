import os
import math
import cv2
import numpy as np
from PIL import Image, ImageEnhance

def detectLp(filename):
    path = './base/' + filename
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img_h, img_w = img.shape[:2]
    org_img = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # color gray
    img = cv2.bilateralFilter(img, 9, 75, 75) # blur filter
    img = cv2.Canny(img, 50, 50) # extract edge
    cv2.imwrite('./canny/' + filename, img)

    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # objects list
    
    rec_box = []; c = []; 
    f_count = 0; select = 0; plate_width = 0;
    for i in range(len(contours)):
        x, y, w, h = cv2. boundingRect(contours[i])
        area = w*h; ratio = float(w)/h;
        # filtering box size << overfitted
        if ratio >= 0.2 and ratio < 1.0 and area >= 2000 and area <= 5000: 
            print("x: ", x, " y: ", y, " w: ", w, " h: ", h)
            c.append((int(x+w/2), int(y+h/2)))
            print("ratio: ", ratio, " area: ", area)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 225, 0), 1)
            rec_box.append(cv2.boundingRect(contours[i]))

    for i in range(len(rec_box)):
        for j in range(len(rec_box)-(i+1)):
            if rec_box[j][0] > rec_box[j+1][0]:
                temp = rec_box[j]
                rec_box[j] = rec_box[j+1]
                rec_box[j+1] = temp

    print(rec_box)
    for m in range(len(rec_box)):
        count = 0
        for n in range(m+1, len(rec_box)-1):
            delta_x = abs(rec_box[n+1][0]-rec_box[m][0])
            if delta_x == 0: delta_x = 1;
            delta_y = abs(rec_box[n+1][1]-rec_box[m][1])
            if delta_y == 0: delta_y = 1;
            gradient = float(delta_y)/float(delta_x)
            if gradient < 0.25: count += 1

        if count > f_count:
            f_count = count; select = m; plate_width = delta_x

    angle = math.atan2(c[0][1]-c[len(c)-1][1], c[0][0]-c[len(c)-1][0]) * 180/math.pi
    if angle > 90: angle -= 180
    rotate_img = cv2.warpAffine(org_img, cv2.getRotationMatrix2D(((c[0][0]+c[1][0])/2, (c[0][1]+c[1][1]/2)), angle, 1), (img_w, img_h))
    # left-top == (0, 0) / [HEIGHT, WIDTH]
    img = rotate_img[rec_box[select][1]-20:rec_box[select][3]+rec_box[select][1]+20, rec_box[select][0]-50:100+rec_box[select][0]+400]
    resize_img = cv2.imwrite('./rslt_detect/resize_'+filename, cv2.resize(img, None,fx=1.8,fy=1.8,interpolation=cv2.INTER_CUBIC+cv2.INTER_LINEAR))

    return resize_img
# class Recognition():
#     def recogLp(self):

filenames = os.listdir('./base')
for filename in filenames:
    detectLp(filename)
print("detection complete")