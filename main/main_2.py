import threading
import argparse
#import importlib
import time
import os
import sys

def writer_thread():
    global close_console
    close_console = False
    s = ''
    while True:
        if close_console:
            break
        old_s = s

        filename = 'tmp.txt'
        points = 0
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                points = f.read()
        s = 'd1 {};  d2 {};  d3 {};  ir {};  rot {};  w {};  d[on {}; f {}; b {}];  {}\n'.format(GPIO.input(components['door_sensors'].DOOR_UP_PIN),
                                                    GPIO.input(components['door_sensors'].DOOR_DOWN_PIN),
                                                    GPIO.input(components['door_sensors'].DOOR_BACK_PIN),
                                                    components['ir_sensors'].show_all(),
                                                    GPIO.input(components['rotator'].ROTATOR_OPTICAL_PIN),
                                                    components['weight'].delta,
                                                    #GPIO.input(components['destroyer'].SENSOR_PIN),
                                                    GPIO.input(components['destroyer'].POWER_PIN),
                                                    GPIO.input(components['destroyer'].FORWARD_PIN),
                                                    GPIO.input(components['destroyer'].BACKWARD_PIN),
                                                    points)
        if s != old_s:
            f = open('1.txt', 'a')
            f.write(s)
            f.close()
        time.sleep(0.02)


class Main_thread:
  def __init__(self):
    self.run = True

  def start(self):
    thrd = threading.Thread(target=self.thread, args=())
    thrd.start()
    thrd.join()

  def stop(self, error_code):
    self.run = False
    data['error_code'] = error_code

  def stop_by_ir(self, error_code):
    self.run = False
    data['error_code'] = error_code
    components['monitor'].state(10) 
    
  def thread(self):
    while self.run:
      data['state_changed'] =  data['old_state'] != data['state']
      if data['state_changed']:
        print("[MAIN_THREAD] Состояние {}".format(data['state']))
        
      data['old_state'] = data['state']
      code, data['state'] = states[data['state']](components, data)
      if code == 0:
        data['error_code'] = data['state']
        data['old_state'] = data['state']
        break
      
    print("[MAIN_THREAD] Ошибка номер {}".format(data['error_code']))
    

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", type=str, default='config')
    ap.add_argument('--console', action='store_true')
    ap.add_argument('--not_rpi', action='store_true') 
    args = vars(ap.parse_args())

    if not args['not_rpi']:
        import RPi.GPIO as GPIO

    path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
    sys.path.insert(0, path)

    if args['console']:
        os.environ['SDL_VIDEO_WINDOW_POS']='1000,0'

    if not args['not_rpi']:
        try:
            import configure_file as config
        except:
            with open('configure_file.py', 'w') as f:
                f.write('from config.config_sortomat_2 import *')
            import configure_file as config
    else:
        from config import config_test as config
      
    components = config.components
    print('[MAIN_THREAD] Компоненты готовы')

    sys.path.insert(0, path)

    states = config.stable_states.states
    states.update(config.unstable_states.states)

    if not os.path.exists(components['SAVE_PATH']):
        os.makedirs(components['SAVE_PATH'])

    data = dict()
    data['error_code'] = None
    data['state'] = 0 
    data['old_state'] = -1 
    data['next_state'] = -1 
    data['state_changed'] = True
    data['check_time'] = 0 
    data['false_things_counter'] = 0 
    data['points'] = 0 
    data['add_points'] = 0 
    data['hand_detection_time'] = 0 
    data['save_path'] = '{}/{}'.format(components['SAVE_PATH'],
                                       len(os.listdir(components['SAVE_PATH'])))
    data['user_id'] = 0

    os.mkdir(data['save_path'])
   
    components['monitor'].state(10)

    if args['console']:
        os.environ['SDL_VIDEO_WINDOW_POS']='0,0'
        os.popen('DISPLAY=":0" lxterminal --geometry=180x35 -t "Debug data" -e watch -n 0.1 -d tail -n 20 1.txt')
        threading.Thread(target=writer_thread, args=()).start()
        
    while True:
        if data['error_code'] is None:
            time.sleep(0.1)
        elif data['error_code'] < 1:
            time.sleep(0.1)
        else:
            break
        is_critical, is_Full = components['us_sensor'].is_Full()
        if components['door_sensors'].all_closed() and not is_Full:
            components['monitor'].state(1)
      
            m = Main_thread()
            components['door_sensors'].stop_function = lambda x : m.stop_by_ir(x)
            components['destroyer'].stop_function = lambda x : m.stop(x)
            m.start()
            components['destroyer'].stop_destroyer()
            components['rotator'].stop() 

    components['monitor'].set_points(int(data['error_code']))
    components['monitor'].state(8)

    if args['console']:
        close_console = True
                 
    components['destroyer'].stop_destroyer()
    components['rotator'].stop()
    
        
    while components['destroyer'].state != 'stop':
        time.sleep(0.05)
    if not args['not_rpi']:
        GPIO.cleanup() 
    print("_______________________________________________________________")
    print("[MAIN_THREAD] Завершение работы")
    sys.exit()
