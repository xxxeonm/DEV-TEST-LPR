import numpy as np
import cv2

def transform():
    img = cv2.imread('./base/403_2975.jpg', cv2.IMREAD_COLOR)
    h, w = img.shape[:2]

    pts1 = np.float32([[0,0], [300,0], [0,300],[300,300]])
    pts2 = np.float32([[0,0], [300,0], [28, 387], [379, 390]])

    m = cv2.getPerspectiveTransform(pts1, pts2)
    img2 = cv2.warpPerspective(img, m, (w, h))
    cv2.imshow('perssssibal', img2)
    cv2.waitKey(0)