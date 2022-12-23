from modules import yolov5
import cv2

class Object_detection:
    def __init__(self, settings):
        
        self.nn = yolov5.Yolov5(model=settings['YOLO_MODEL'],
                                labels=settings['YOLO_CLASSES'],
                                input_shape=settings['YOLO_MODEL_INPUT_SHAPE'])
        
        self.nn.model.conf = settings['YOLO_MODEL_CONF']
        self.nn.model.iou = settings['YOLO_MODEL_IOU']
        self.nn.model.max_det = settings['YOLO_MODEL_MAX_DET']
        
    
    def run(self, frame, data):        
        data['image'] = frame.copy()
        #data['chaos'] = self.nn2.detect(cv2.resize(frame, (320, 320)))
         
        data['datections'] = self.nn.detect(data['image'])
        
        return data

