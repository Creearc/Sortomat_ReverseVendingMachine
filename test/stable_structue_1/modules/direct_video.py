import cv2
import numpy as np
import threading
import time

template = np.zeros((736, 736, 3), np.uint8)

class Video():
    def __init__(self, path):
        self.path = path
        self.cam = cv2.VideoCapture(self.path)

        self.frame_count = int(self.cam.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_rate = int(self.cam.get(cv2.CAP_PROP_FPS))
        self.w = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.frame_number = 0
        self.first_frame = 0
        self.last_frame = self.frame_count
        self.step = 1


    def get_img(self):

        if self.frame_number < self.first_frame:
            self.frame_number = self.first_frame

        if self.frame_number >= self.last_frame:
            self.frame_number = self.first_frame
            

        self.cam.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number)
        self.frame_number += self.step
        
        ret, img = self.cam.read()

        return img
    

class Direct_video():
    def __init__(self, path_to_video_1):
        self.c1 = Video(path_to_video_1)


    def get_img(self):
        img = self.c1.get_img().copy()

        return img
