import os
import cv2

class ImageSaver():
  def __init__(self, path='output_photos'):
    if not os.path.exists(path):
      os.mkdir(path)

    self.path = '{}/{}'.format(path, len(os.listdir(path)))
    os.mkdir(self.path)

  def save(self, img, results):
    cv2.imwrite('{}/{} .png'.format(self.path,
                                    len(os.listdir(self.path)),
                                    ' '.join(results)), img)

