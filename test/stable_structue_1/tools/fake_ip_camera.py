import threading
import time

import video_module
import zmq_module


def video_thread(path_to_video=''):
    c = video_module.Video(path_to_video)
    fps = 1 / 25
    t = time.time()
    while True:
        for frame_number, img in c.get_img():
            time.sleep(fps)
            serv.put_img(img)
            t = time.time()
    



if __name__ == '__main__':
    path_to_video = 'videos/Tue Jul  5 15_11_34 2022.mp4'
    #path_to_video = 'videos/calibrate.avi'
    
    serv = zmq_module.ZMQ_transfer(ip='0.0.0.0', port=5058)
    serv.run()

    threading.Thread(target=video_thread, args=(path_to_video, )).start()
