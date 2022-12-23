

class Get_frame:
    def __init__(self, settings):
        if settings['CAMERA_TYPE'] == 'debug':
            from modules import zmq_module
            self.video_source = zmq_module.ZMQ_receiver(ip=settings['CAMERA_IP'],
                                                        port=settings['CAMERA_PORT'])
            self.video_source.run()

        elif settings['CAMERA_TYPE'] == 'ip':
            from modules import ip_cam_module
            self.video_source = ip_cam_module.IPCamera(settings['CAMERA_SRC'], True)
            self.video_source.start()

        elif settings['CAMERA_TYPE'] == 'direct_video':
            from modules import direct_video
            self.video_source = direct_video.Direct_video(settings['PATH_TO_VIDEO'])

        elif settings['CAMERA_TYPE'] == 'usb':
            from modules import usb_cam_module
            self.video_source = usb_cam_module.Camera(settings['CAMERA_SRC'],
                                                      settings['WIDTH'],
                                                      settings['HIGHT'])
            self.video_source.start()

    
    def run(self, data):
        frame = self.video_source.get_img()
        
        return frame, data
