import sys
import os
import cv2
import numpy as np
import time
import threading


FRAMES_TO_RECORD = 10000
LOGIN = 'admin'
PASSWORD = 'admin'
IP = '192.168.0.20'
PORT = 8554


class IPCamera:
    def __init__(self, src="rtsp://admin:admin@192.168.0.20:8554/CH001.sdp",
                 debug=False):
        self.src = src
        print(src)
        self.lock = threading.Lock()
        self.debug = debug
        self.img = None


    def connect(self):
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
        self.cam = cv2.VideoCapture(self.src, cv2.CAP_FFMPEG)


    def get_img(self):
        with self.lock:
            return self.img


    def process(self):
        self.connect()

        mx = 500
        i = 0
        t = time.time()
        
        while True:
            ret, img = self.cam.read()    
            if not ret:
                print(time.ctime(), 'No frame')
                time.sleep(5.0)
                self.connect()
                continue
            
            with self.lock:
                self.img = img.copy()
            
            if self.debug:
                i += 1
                if i == mx:
                    i = 0
                    fps = mx / (time.time() - t)
                    t = time.time()
                    print('Camera quality = {} FPS = {}'.format(int(camera_quality(img)), fps))
     

    def start(self):
        print('[CAMERA] Ready!')
        c = threading.Thread(target=self.process, args=())
        c.start()


def video_record(FRAMES_TO_RECORD=1000):
    global c, img_buf, lock
    w, h = 1920, 1080
    frame_rate = 30
    codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    vid_out = cv2.VideoWriter('{}.mp4'.format(str(time.time()).replace('.', '_')),
                              codec, frame_rate,
                              (w, h))
    img = None
    while img is None:
        img = c.get_img()

    print('Record!')

    for i in range(FRAMES_TO_RECORD):
        print(i)

        img = c.get_img()

        #out = functions.fix_collision(img)
        out = cv2.resize(img, (1920, 1080), interpolation = cv2.INTER_AREA)

        vid_out.write(out)
        time.sleep(1/25)

    vid_out.release()
    print('Finish!')


if __name__ == '__main__':
    lock = threading.Lock()

    img_buf = None

    c = ip_cam_module.IPCamera("rtsp://{}:{}@{}:{}/CH001.sdp".format(LOGIN, PASSWORD, IP, PORT))
    c.start()
    threading.Thread(target=video_record, args=(FRAMES_TO_RECORD, )).start()

    
