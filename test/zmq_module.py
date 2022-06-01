import threading
import time
import zmq
import numpy as np
import cv2
import pickle
from multiprocessing import Process, Value, Queue

class Camera:
  def __init__(self, src=0, WIDTH=1280, HEIGHT=720,
               CODEC=cv2.VideoWriter_fourcc('M','J','P','G')):
    self.src = src
    self.WIDTH = WIDTH
    self.HEIGHT = HEIGHT
    self.CODEC = CODEC

    self.cam = cv2.VideoCapture(self.src)
    self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
    self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
    self.cam.set(cv2.CAP_PROP_FOURCC, self.CODEC)
    self.cam.set(cv2.CAP_PROP_FPS, 25)
    self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    self.img_s = Queue(2)

  def get_img(self):
    while self.img_s.empty():
      pass
    return self.img_s.get()

  def process(self):
    
    while True:
      ret, img = self.cam.read()    
      if not ret:
        continue
      if self.img_s.full():
        self.img_s.get()
      self.img_s.put(img)
   
  def start(self):
    c = Process(target=self.process, args=())
    c.start()


class ZMQ_receiver:
    def __init__(self, ip='127.0.0.1', port=5003):
        self.ip = ip
        self.port = port

        self.img = None
        self.lock = threading.Lock()

    def connect(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.RCVTIMEO = 1000
        self.socket.connect("tcp://{}:{}".format(self.ip, self.port))

    def run(self):
        threading.Thread(target=self.zmq_thread, args=()).start()

    def zmq_thread(self):
        self.connect()

        print('[ZMQ receiver] Server is ready')

        while True:    
            try:
                self.socket.send_string('image', zmq.NOBLOCK)
                msg = self.socket.recv() 
            except Exception as e:
                print(e)
                print('[ZMQ receiver] No connection')
                self.connect()
                time.sleep(0.1)
                continue
            
            img = pickle.loads(msg)
            if img is None:
                continue
            
            with self.lock:
                self.img = img.copy()

    def get_img(self):
        with self.lock:
            img = self.img
        return img
        

class ZMQ_transfer:
    def __init__(self, ip='10.11.0.1', port=5003):
        self.ip = ip
        self.port = port

        self.img = None
        self.lock = threading.Lock()

    def bind(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.RCVTIMEO = 1000
        self.socket.bind("tcp://{}:{}".format(self.ip, self.port))

    def run(self):
        threading.Thread(target=self.zmq_thread, args=()).start()

    def zmq_thread(self):
        self.bind()

        print('[ZMQ transfer] Server is ready')

        while True:
            try:
                msg = self.socket.recv().decode() 
            except Exception as e:
                print(e)
                print('[ZMQ transfer] No connection')
                time.sleep(0.1)
                continue
            
            with self.lock:
                img = self.img

            msg = pickle.dumps(img)
            self.socket.send(msg, zmq.NOBLOCK)

    def put_img(self, img):
        with self.lock:
            if not (img is None):
                self.img = img.copy()
            else:
                print('[ZMQ transfer] Img is None')


if __name__ == '__main__':
    c = Camera()
    c.start()

    serv = ZMQ_transfer()
    serv.run()
    
            
    while True:
            frame = c.get_img()

            cv2.putText(frame, str(time.time()),
                        (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.6,
                        (0, 0, 255), 2)
            
            serv.put_img(frame)

