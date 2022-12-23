import cv2
import imutils
import numpy as np
import time
from modules import functions
from modules import mongo_functions
from modules import json_unpacker

class Data_processing:
    def __init__(self, settings):
        self.OUTPUT_PATH = settings['OUTPUT_PATH']
        self.debug = settings['DEBUG']
        self.settings = settings

        
    def run(self, data):  
        detections, data['image'] = nn_analisis(data['datections'],
                                               data['image'],
                                               data,
                                               self.settings)      

        return data

  

def extract_object(img):
    tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #tmp = functions.adjust_gamma(tmp, gamma=3.0)
    #tmp = cv2.equalizeHist(tmp)
    tmp = imutils.adjust_brightness_contrast(tmp,
                                             brightness=-150.0,
                                             contrast=250.0)
    tmp = cv2.threshold(tmp, 170, 255, cv2.THRESH_BINARY)[1]
    tmp = cv2.dilate(tmp, np.ones((3, 3), np.uint8), iterations=1)
    cnts = cv2.findContours(tmp, cv2.RETR_EXTERNAL,
                          cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    #tmp = cv2.cvtColor(tmp, cv2.COLOR_GRAY2BGR)

    result = np.zeros((tmp.shape[0], tmp.shape[1], 3), np.uint8)
    if len(cnts) == 0:
        return None, result

    c = max(cnts, key=cv2.contourArea)

    cv2.drawContours(image=result,
                     contours=[c],
                     contourIdx=0,
                     color=(255, 255, 255),
                     thickness=-1,
                     lineType=cv2.LINE_AA)
    
    result = cv2.blur(result, (5, 5))
    
    (x, y, w, h) = cv2.boundingRect(c)
    return [x, y, w, h], result



def nn_analisis(detections, img, data, settings):
    H, W = img.shape[:2]
    result_img = img.copy()
    for detection in detections:        
        x, y = int(W * detection[0]), int(H * detection[1])
        w, h = int(W * detection[2]), int(H * detection[3])
        class_name = settings['YOLO_CLASSES'][int(detection[-1])]
        
        x, y = x - w // 2, y - h // 2

        cv2.rectangle(result_img,
                          (x, y),
                          (x + w, y + h),
                          (255, 255, 100),
                          5)

            
        functions.print_text(result_img,
                             class_name,
                             (x, y),
                             (255, 255, 255),
                             1.0, 2,
                             no_back=False)


    return detections, result_img
