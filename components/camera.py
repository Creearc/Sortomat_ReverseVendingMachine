# Модуль камеры
import sys
import os
import cv2
import imutils
import numpy as np
import time
from multiprocessing import Process, Value, Queue

# Проверка размытости изображения
def is_camera_ok(img, threshold=100):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  if cv2.Laplacian(gray, cv2.CV_64F).var() < threshold:
    return False
  else:
    return True


def adjust_gamma(image, gamma=1.0):
  invGamma = 1.0 / gamma
  table = np.array([((i / 255.0) ** invGamma) * 255
    for i in np.arange(0, 256)]).astype("uint8")
  return cv2.LUT(image, table)


# Проверка наличия объекта на изображении
def is_object_red(img, debug=False, show=False):
  out = img[300 : 420, 200 : 980]
  out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
  old = imutils.resize(out, width=300, inter=cv2.INTER_NEAREST)
  out = adjust_gamma(out, 15.5)
  out = imutils.resize(out, width=300, inter=cv2.INTER_NEAREST)
  out = cv2.GaussianBlur(out, (11, 11), 0)
  
  ret, out = cv2.threshold(out, 225, 255, cv2.THRESH_BINARY)

  cnts = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = imutils.grab_contours(cnts)
  mx = 0
  for cnt in cnts:
    if cv2.contourArea(cnt) > mx:
      mx = cv2.contourArea(cnt)
      
  if debug:
    print('Max obj size {}'.format(mx))
  if show:
    cv2.imshow('is_object', np.vstack([out, old]))
    cv2.waitKey(1)
    
  if mx > 100:
    return True
  else:
    return False

def is_object_blue(img, debug=False, show=False):
  out = img[300 : 420, 200 : 980]
  out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
  old = imutils.resize(out, width=300, inter=cv2.INTER_NEAREST)
  out = adjust_gamma(out, 6.5)
  out = imutils.resize(out, width=300, inter=cv2.INTER_NEAREST)
  out = cv2.GaussianBlur(out, (7, 7), 0)
  
  ret, out = cv2.threshold(out, 225, 255, cv2.THRESH_BINARY)

  cnts = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = imutils.grab_contours(cnts)
  mx = 0
  for cnt in cnts:
    if cv2.contourArea(cnt) > mx:
      mx = cv2.contourArea(cnt)
      
  if debug:
    print('Max obj size {}'.format(mx))
  if show:
    cv2.imshow('is_object', np.vstack([out, old]))
    cv2.waitKey(1)
    
  if mx > 30:
    return True
  else:
    return False


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
    self.cam.set(cv2.CAP_PROP_FPS, 60)
    self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    self.img = None
    self.wait = Queue(2)
    self.img_s = Queue(2)

  def get_img(self):
    while self.img_s.empty():
      pass
    return self.img_s.get()

  def process(self):
    while True:
      ret, self.img = self.cam.read()    
      if not ret:
        continue
      if self.img_s.full():
        self.img_s.get()
      self.img_s.put(self.img)
      #print(1)
      
  def start(self):
    c = Process(target=self.process, args=())
    c.start()
    time.sleep(2.0)


if __name__ == '__main__':
  import time
  c = Camera()
  c.start()
  while True:
    img = c.get_img()
    #print(is_object(frame, True, True))
    print(is_object_red(img, True, True))

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
      break

  cv2.destroyAllWindows()

