import math
import numpy as np
import cv2
import tensorflow.compat.v1 as tf #.v1
#import tensorflow._api.v2.compat.v1 as tf
import os
from tensorflow import keras
try:
    import tflite_runtime.interpreter as tflite
except:
    import tensorflow.compat.v1.lite as tflite

import keras.backend as K
import random
from image_component import transform_img_tf, preprocess_img

class Model:
  def __init__(self, mm):
      self.model = None
      self.image_shape = None

      #model_path = "/home/pi/main/m2.tflite"
      model_path = mm#"/Users/akokoulin/Desktop/Sortomat/_cleaner/model_AR.tflite"#"/home/pi/main/model_AR.tflite"
      self.debug = True
      self.tflite = True
      self.preprocessing = True
      self.data_format='channels_last'

      self.labels = ['al__Other', 'hdpe__Chemistry', 'Other__Other2', 'pet__Blue', 'pet__Brown', 'pet__Chemistry', 'pet__Green', 'pet__Milk', 'pet__MilkWhite', 'pet__Oil', 'pet__Transparent']
      self.n_classes = len(self.labels)
      self.padding_bottom = 250
      self.padding_top = 300
      self.padding_left = 250
      self.padding_right = 250
      #self.padding_bottom = 300
      #self.padding_top = 330
      #self.padding_left = 280
      #self.padding_right = 280
      self.padding = False
      if self.model is None:
          print('Model loading')
          if self.tflite:
              interpreter = tf.lite.Interpreter(model_path=model_path)
              interpreter.allocate_tensors()
              self.input_details = interpreter.get_input_details()
              self.output_details = interpreter.get_output_details()
              self.input_shape = self.input_details[0]['shape']
              self.input_dtype = self.input_details[0]['dtype']
          else:
              self.model.load(model_path)
              self.input_shape = (448, 224, 3)#(224, 224, 3)
              self.input_dtype = np.float32
          self.image_shape = self.input_shape[1:]
          self.model = interpreter if self.model is None else self.model
          tf.enable_eager_execution()


  def preprocess_fn(self, image):
      newSize = self.image_shape[:2]
      if self.padding:    
        image = image[self.padding_top:-self.padding_bottom, self.padding_left:-self.padding_right, ...]
      #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      #image = transform_img_tf(image, image.shape, newSize, self.input_dtype)
      image = tf.image.resize(image, newSize)
      if self.preprocessing:
        image = preprocess_img((image.numpy()).astype(np.uint8), img_width=self.input_shape[0], img_height=self.input_shape[1])
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      #cv2.imshow("Image", image)
      #cv2.waitKey(1)
      image = tf.cast(image, dtype=self.input_dtype)
      if self.input_dtype == tf.float32 or self.input_dtype == tf.float64 or self.input_dtype == tf.float16 or self.input_dtype == tf.bfloat16:
        image = image * (1. / 255)
      return image

  def concat_fn(self, changed_images):
      if self.data_format == 'channels_last':
          image = tf.concat(changed_images, axis=1)
          image = tf.image.resize(image, self.image_shape[:2])
      else:
          image = tf.concat(changed_images, axis=2)
          image = tf.image.resize(image, self.image_shape[1:])
      image = tf.reshape(image, self.image_shape)
      return image

  def classify_images(self, origImages):
      images = []
      for origImage in origImages:
          images.append(self.preprocess_fn(origImage))
      image = self.concat_fn(images).numpy()
      image = np.expand_dims(image, axis=0).astype(self.input_dtype)
      if tflite:
          self.model.set_tensor(self.input_details[0]['index'], image)
          self.model.invoke()
          results = {"net_output": self.model.get_tensor(self.output_details[-1]['index'])[0]}
      else:
          results = self.model(image)
      prob = np.squeeze(results["net_output"])
      predicted_class = np.argmax(prob)

      pred_probas_argmax = self.labels[predicted_class]
      if self.debug:
          print('Model')
          print(prob[predicted_class])
          print(self.labels[predicted_class])
      return self.labels[predicted_class]
