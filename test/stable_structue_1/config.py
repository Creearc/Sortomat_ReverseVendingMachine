import os
import cv2
import numpy as np

np.random.seed(18)

settings = dict()

settings['DEBUG'] = True

if settings['DEBUG']:
    settings['CAMERA_TYPE'] = 'debug'
    settings['CAMERA_IP'] = '192.168.0.100'
    settings['CAMERA_PORT'] = 5058
    
    settings['OUTPUT_PATH'] = 'static/data/'
##    settings['CAMERA_TYPE'] = 'direct_video'
##    settings['PATH_TO_VIDEO_1'] = 'tools/videos/1.avi'
    
else:
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    settings['CAMERA_TYPE'] = 'usb'
    settings['CAMERA_SRC'] = 0
    
    settings['OUTPUT_PATH'] = 'static/data/'

settings['RECORD_FILE'] = 'result.avi'    
    
settings['STREAM_IP'] = '0.0.0.0'
settings['STREAM_PORT'] = 5005

settings['YOLO_MODEL'] = 'models/sortomat_s_736_0.pt'
settings['YOLO_CLASSES'] = ['al', 'glass', 'hdpe_chemistry', 'other', 'pet_blue',
                            'pet_brown', 'pet_chemistry', 'pet_colored', 'pet_green',
                            'pet_milk', 'pet_milk_white', 'pet_oil', 'pet_transparent',
                            'tetrapak']

settings['YOLO_COLORS'] = np.random.uniform(0, 255,
                                            size=(len(settings['YOLO_CLASSES']),
                                                  3))
settings['YOLO_MODEL_INPUT_SHAPE'] = 736
settings['YOLO_MODEL_CONF'] = 0.15
settings['YOLO_MODEL_IOU'] = 0.05
settings['YOLO_MODEL_MAX_DET'] = 10


settings['WIDTH'] = 1280
settings['HIGHT'] = 720


data = dict()
data['stop'] = False

