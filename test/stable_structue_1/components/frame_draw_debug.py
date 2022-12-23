import time
import cv2
import imutils

from modules import functions

class Frame_draw_debug:
    def __init__(self, settings):
        self.debug = settings['DEBUG']
        self.t = time.time()
        self.record = False

        if 'RECORD_FILE' in settings.keys():
            codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            self.vid_out = cv2.VideoWriter(settings['RECORD_FILE'],
                                          codec, 25,
                                          (settings['WIDTH'],
                                           settings['HIGHT']))
            self.record = True
        

    def run(self, data):
        result = data['image'].copy()        

        self.t = 1 / (time.time() - self.t)
        functions.print_text(result, 'FPS {}'.format(int(self.t)),
                             (50, 100),
                             (255, 255, 255),
                             1.6, 5)

        functions.print_text(result, time.ctime(),
                            (50, 50),
                            (255, 255, 255),
                            1.6, 5)

        data['result'] = result.copy()
        
        if True: 
                
            cv2.imshow('',  cv2.resize(result, (1920 // 2, 1080 // 2)))
            key = cv2.waitKey(1)
            if key == ord('q') or key == 27:
                cv2.destroyAllWindows()
                data['stop'] = True

        if self.record:
            self.vid_out.write(result)
                
        self.t = time.time()
        return data
