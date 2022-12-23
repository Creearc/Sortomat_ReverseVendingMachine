import torch
import numpy as np


class Yolov5:
    def __init__(self, model='best.pt', labels=['smallhole', 'zakor', 'zazor'],
                 input_shape=640):
        # Model
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print('[YOLOv5] Device is {}'.format(device))
        self.model = torch.hub.load('yolov5', 'custom',
                                    path=model, force_reload=True,
                                    source='local'
                                    )
        self.labels = labels
        self.input_shape = input_shape
        
        np.random.seed(18)
        self.colors = np.random.uniform(0, 255, size=(len(self.labels), 3))

    def detect(self, img):
        results = self.model(img, size=self.input_shape)
        detections = results.xywhn[0].tolist()
            
        return detections

        
