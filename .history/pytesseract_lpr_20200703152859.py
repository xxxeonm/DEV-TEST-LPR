#!/usr/bin/etc python

import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
from PIL import ImageEnhance

import time

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class Recognition():
     def ExtractNumber(self, filename):
          print(filename)
          # print('../../../DATASETS/lp_korea/' + filename)
          t0 = time.time()
          img = cv2.imread('./base/'+filename, cv2.IMREAD_COLOR)
          # img = cv2.imread('../../DATASETS/lp_kor/google/' + filename, cv2.IMREAD_COLOR)
          copy_img=img.copy()
          copy_img2 = img.copy()
          img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
          # blur = cv2.GaussianBlur(img2,(3,3),0)
          # blur = cv2.medianBlur(img2, 1)
          blur = cv2.bilateralFilter(img2, 9, 75, 75)
          canny=cv2.Canny(blur,50,50)
          cv2.imwrite('./canny/'+filename, canny)
          contours,hierarchy  = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

          box1=[]
          f_count=0
          select=0
          plate_width=0

          for i in range(len(contours)):
               cnt=contours[i]          
               area = cv2.contourArea(cnt)
               x,y,w,h = cv2.boundingRect(cnt)
               rect_area=w*h  #area size
               aspect_ratio = float(w)/h # ratio = width/height

               # box size
               if (aspect_ratio>=0.2)and(aspect_ratio<1.0)and(rect_area>=2000)and(rect_area<=5000): 
               # if  (aspect_ratio>=0.2)and(aspect_ratio<=1.0)and(rect_area>=500)and(rect_area<=3000): 
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)
                    box1.append(cv2.boundingRect(cnt))
          for i in range(len(box1)): ##Buble Sort on python
               for j in range(len(box1)-(i+1)):
                    if box1[j][0]>box1[j+1][0]:
                         temp=box1[j]
                         box1[j]=box1[j+1]
                         box1[j+1]=temp
          print(box1)
    
          # to find number plate measureing length between rectangles
          for m in range(len(box1)):
               count=0
               for n in range(m+1,(len(box1)-1)):
                    delta_x=abs(box1[n+1][0]-box1[m][0])
                    if delta_x > 150:
                         break
                    delta_y =abs(box1[n+1][1]-box1[m][1])
                    if delta_x ==0:
                         delta_x=1
                    if delta_y ==0:
                         delta_y=1           
                    gradient =float(delta_y) /float(delta_x)
                    if gradient<0.25:
                        count=count+1
               # measure number plate size         
               if count > f_count:
                    select = m
                    f_count = count
                    plate_width=delta_x
          cv2.imwrite('./snake/' + filename,img)
          
          # crop size
          number_plate=copy_img[box1[select][1]-10:box1[select][3]+box1[select][1]+20,box1[select][0]-10:100+box1[select][0]+50] 
          # number_plate=copy_img[box1[select][1]-10:box1[select][3]+box1[select][1]+30,box1[select][0]-150:100+box1[select][0]+150] 
          resize_plate=cv2.resize(number_plate,None,fx=1.8,fy=1.8,interpolation=cv2.INTER_CUBIC+cv2.INTER_LINEAR) 

          cv2.imshow('resize_'+filename, resize_plate)

          ### RECOGNITION ###

          plate_gray=cv2.cvtColor(resize_plate,cv2.COLOR_BGR2GRAY)
          # tmp_plate = cv2.equalizeHist(plate_gray)
          tmp_plate = cv2.morphologyEx(plate_gray, cv2.MORPH_CLOSE, kernel=np.ones((3,3), np.uint8))
          # ret,th_plate = cv2.threshold(tmp_plate,150,255,cv2.THRESH_BINARY)
          
          # cv2.imwrite('./plate_th/' + filename, th_plate)
          _, img_th_plateresult = cv2.threshold(tmp_plate, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
          # cv2.imwrite('./img_result/' + filename, th_plate)

          cv2.imwrite('./threshold/'+filename, img_th_plateresult)
          
          # result = pytesseract.image_to_string(Image.open('./plate_th/' + filename), lang='kor', config='--psm 7 --oem 2')
          result = pytesseract.image_to_string(img_th_plateresult, lang='kor_lp_gen', config='--psm 7 --oem 2')
          # print(result)
          result_chars = ''; result_idx = 0
          for c in result:
               if (ord(c) >= ord('가') and ord(c) <= ord('힣')) or c.isdigit():
                    result_chars += c

          print("time: ", time.time() - t0)
          return(result_chars.replace(" ",""))


# filenames = os.listdir('../../DATASETS/lp_kor/google')
filenames = os.listdir('./base')
for filename in filenames:
     print(Recognition().ExtractNumber(filename))
     print()

# filename = '31gj4150.bmp'
# Recognition().ExtractNumber(filename)