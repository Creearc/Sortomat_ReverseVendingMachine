import cv2
import numpy as np
import random
import tensorflow.compat.v1 as tf
#import tensorflow._api.v2.compat.v1 as tf
from common_params import get_common_params
from feature_codes import *

def transform_img_tf(image, origImageShape, newSize, dtype):
    image = tf.cast(image, dtype=dtype)
    if dtype == tf.float32 or dtype == tf.float64 or dtype == tf.float16 or dtype == tf.bfloat16:
        image = image * (1. / 255) #преобразование в float32 или bfloat16 должно проивзодится именно так (cast, /255.), иначе обучается долльше на 30% и плохо сходится

    image = tf.reshape(image, origImageShape)
    ''''offset_height = tf.cast(tf.math.multiply(tf.constant(bounding_box_y[0]), tf.cast(tf.gather_nd(origImageShape, [0]), tf.float32)), tf.int32)
    offset_width = tf.cast(tf.math.multiply(tf.constant(bounding_box_x[0]), tf.cast(tf.gather_nd(origImageShape, [1]), tf.float32)), tf.int32)
    target_height = tf.cast(tf.math.multiply(tf.constant(bounding_box_y[1] - bounding_box_y[0]), tf.cast(tf.gather_nd(origImageShape, [0]), tf.float32)), tf.int32)
    target_width = tf.cast(tf.math.multiply(tf.constant(bounding_box_x[1] - bounding_box_x[0]), tf.cast(tf.gather_nd(origImageShape, [1]), tf.float32)), tf.int32)
    image = tf.image.crop_to_bounding_box(image, offset_height, offset_width, target_height, target_width)''' #crop_to_bounding_box не работает

    image = tf.image.resize(image, newSize)
    image = tf.cast(image, dtype=dtype)
    return image

def transform_img(img):
    img_width = get_common_params('img_width')
    img_height = get_common_params('img_height')
    #Histogram Equalization
    if getPreprocessingCode(4):
      img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
      img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
      img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

    return img

def preprocess_img(img, img_width=224, img_height=224):
  if getPreprocessingCode(7):
    img = cv2.GaussianBlur(img, (21, 21), 0)
  if getPreprocessingCode(5):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img[:, :, 2] = np.ones(shape=(img_width, img_height), dtype=np.uint8)*128
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
  if getPreprocessingCode(6):
    img = np.array((img / 2 - cv2.filter2D(img, -1, np.ones((37, 37), np.float32) / (37 * 37)) / 2) + 128, np.uint8)
  return img

def full_transform_img(img, preprocessing=True):
    img = transform_img(img)
    img = rollaxis_img(img)
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 0, 1)
    if preprocessing:
      img = preprocess_img(img)
    return img

def rollaxis_img(img):
    #image is numpy.ndarray format. BGR instead of RGB
    return np.rollaxis(img, 2)

def read_images(img_paths, preprocessing=True):
  x_set=np.empty(tuple([0]+get_common_params('image_shape')), dtype=np.uint8)
  temp_x_set=[]
  n=0
  h=100
  for in_idx, img_path in enumerate(img_paths):
    n+=1
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if img is None:
      continue
    img = full_transform_img(img, preprocessing=preprocessing)
    temp_x_set.append(img)
    #print(n)
    if n%h==0: #массив numpy занимает меньше памяти, чем list, поэтому используется массив; если заранее размер массива не известен, запролнять его желательно частями, так как list занимает достаточно много памяти и все данные могут не влезть в память, а поэлементо добавлять значения в массив неразумно, так как добавление элементов в массив numpy занимает достаточно много времени
      x_set=np.append(x_set, temp_x_set, axis=0)
      temp_x_set=[]
  if n%h!=0:
    x_set=np.append(x_set, temp_x_set, axis=0)
    temp_x_set=[]
  return x_set

def concatenate_images(left, right):
  if get_common_params('data_format') == 'channels_last':
    result = np.concatenate((left, right), axis=1)
  else:
    result=np.concatenate((left, right), axis=2)
  return result

def resize_img(img):
  return cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

def show_img(name, img):
  cv2.imshow(name, img)

def balance_up(xSet, ySet):
  nByClass = [len(np.where(ySet == i)[0]) for i in range(get_common_params('n_classes'))]
  biggestClass = np.where(nByClass == np.amax(nByClass))[0][0]
  for nClass in range(get_common_params('n_classes')):
    if nByClass[nClass] < nByClass[biggestClass] and nByClass[nClass] > 0:
      xSetByClass = xSet[np.where(ySet == nClass)[0]]
      nCopy = nByClass[biggestClass] - nByClass[nClass]
      indexes = list(range(nByClass[nClass]))
      random.shuffle(indexes)
      c = np.zeros(shape=(nCopy,), dtype = np.int64)
      b = np.array([nClass] * nCopy)
      for idx, i in enumerate(b):
        c[idx] = i
      ySet = np.append(ySet, c, axis = 0)
      xSet = np.append(xSet, xSetByClass[indexes * (nCopy // nByClass[nClass]) + indexes[:(nCopy % nByClass[nClass])]], axis = 0)
  return xSet, ySet

def shuffle_sets(x_set, y_set):
  r = [i for i in range(x_set.shape[0])]
  random.shuffle(r)
  x_set = x_set[r]
  y_set = y_set[r]
  return x_set, y_set
        
