import cv2
import os
import numpy as np
import imutils
import time


def roi(img):
    #crange = [0,0,0, 0,0,0]
    crop_img = img[150:610, 80:1020].copy()
    hsv = crop_img.copy()

    hsv = cv2.GaussianBlur(hsv, (11, 11), 0)  
    hsv = cv2.dilate(hsv, None, iterations=2) 

    # считываем значения бегунков
    # параметры
    # VVVVVVVVVVVVVVVVVVVVVVVVVVVV
    r1 = 0
    g1 = 0
    b1 = 0
    r2 = 150
    g2 = 170
    b2 = 255
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # формируем начальный и конечный цвет фильтра
    h_min = np.array((b1, g1, r1), np.uint8)
    h_max = np.array((b2, g2, r2), np.uint8)

    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h_min, h_max)
    thresh1 = (255-thresh)
    thresh1 = cv2.dilate(thresh1, None, iterations=6) #2

    # contours
    cnts = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    min_X=1000
    max_X=0
    min_Y=500
    max_Y=0

    for cc in cnts:
      (x, y, w, h) = cv2.boundingRect(cc)
      if (cv2.contourArea(cc) > 100):
        cnt_img = crop_img[y-10:y+h+20, x-10:x+w+20].copy()
        if cnt_img.size>0:
          v = cv2.Laplacian(cnt_img, cv2.CV_64F).var()
          if v>84:
            #cv2.rectangle(crop_img, (x-20, y-20), (x + w+40, y + h+40), (0, 255, 0), 2)
            if (x>=30)and(y>=30): 
              if max_X<x+w:
                max_X=x+w
              if min_X>x:
                min_X=x
              if max_Y<y+h:
                max_Y=y+h
              if min_Y>y:
                min_Y=y

    min_X = min_X-20
    min_Y = min_Y-20
    max_X = max_X+20
    max_Y = max_Y+20
    curW = max_X-min_X
    curH = max_Y-min_Y

    if curH*2>curW:
      min_X = int(min_X-((curH*2 - curW)/2))
      if min_X<0:
        min_X=0
      curW = int(curH*2)
      max_X = int(min_X+curW)

    if curH*2<curW:
      min_Y = int(min_Y-((curW - curH*2)/2))
      if min_Y<0:
        min_Y=0
        
      curH = int(curW/2)
      max_Y = int(min_Y + curH)

    result = crop_img[min_Y : max_Y, min_X : max_X].copy()
    #cv2.imshow('result', result)
    #cv2.waitKey(1)
    return result


if __name__ == '__main__':
    file_path = '1.png'
    img = cv2.imread(file_path) 
    img = imutils.resize(img, height=720, width=1280) 

    while True:

        cv2.imshow('result', roi(img))
        cv2.imshow('img', img)

        ch = cv2.waitKey(5)

        if ch == 27:
            break


    cv2.destroyAllWindows()
