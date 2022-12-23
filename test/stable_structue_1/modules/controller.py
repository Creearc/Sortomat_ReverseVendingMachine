import snap7
import time

class Controller:
    def __init__(self, enable=False):
        import snap7
        
        self.enable = enable
#        self.enable = True
        settings = dict()
        settings['ENCODER_IP'] = '192.168.0.149'
        settings['ENCODER_RACK'] = 0
        settings['ENCODER_SLOT'] = 1

        self.plc = snap7.client.Client()
        if True:
            self.plc.connect(settings['ENCODER_IP'],
                 settings['ENCODER_RACK'],
                 settings['ENCODER_SLOT'])


            self.plc.get_connected()        

            data1 = bytearray(1)
            snap7.util.set_bool(data1,0,0,False)
            self.plc.mb_write(0, 1, data1)


    def stop_line(self):
        if self.enable:
            data1 = bytearray(1)
            snap7.util.set_bool(data1,0,0,True)
            self.plc.mb_write(0, 1, data1)
            time.sleep(2.0)
            snap7.util.set_bool(data1,0,0,False)
            self.plc.mb_write(0, 1, data1)


if __name__ == "__main__":
    c = Controller(True)
#    c.stop_line()
    time.sleep(2.0)
    c = Controller(True)
    
