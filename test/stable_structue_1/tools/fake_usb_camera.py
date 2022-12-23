import threading
import time

import usb_cam_module
import zmq_module


def video_thread():
    c = usb_cam_module.Camera(0)
    c.start()
    
    t = time.time()
    while True:
        img = c.get_img()
        if img is None:
            print('empty')
            continue

        serv.put_img(img)
        t = time.time()
    



if __name__ == '__main__':
    
    serv = zmq_module.ZMQ_transfer(ip='0.0.0.0', port=5058)
    serv.run()

    threading.Thread(target=video_thread, args=()).start()

