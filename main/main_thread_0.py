import threading
import time
import os
import sys
path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
sys.path.insert(0, path)

import RPi.GPIO as GPIO
from config import config
  
components = config.components
print('[MAIN_THREAD] Компоненты готовы')

sys.path.insert(0, path)
from config import stable_states
from config import unstable_states

states = stable_states.states
states.update(unstable_states.states)

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
  components['monitor'].state(10) 
  while True:
    if components['door_sensors'].all_closed():
      components['monitor'].state(1)
      
      m = Main_thread()
      components['door_sensors'].stop_function = lambda x : m.stop_by_ir(x)
      components['destroyer'].stop_function = lambda x : m.stop(x)
      m.start()
      components['destroyer'].stop_destroyer()
      components['rotator'].stop() 
    else:
      # 0 - storage is full  -1 - doors
      if data['error_code'] is None:
        time.sleep(0.1)
      elif data['error_code'] < 1:
        time.sleep(0.1)
      else:
        break

  components['monitor'].set_points(data['error_code'])
  components['monitor'].state(8) 
                 
  components['destroyer'].stop_destroyer()
  components['rotator'].stop()  
  GPIO.cleanup() 
  print("_______________________________________________________________")
  print("[MAIN_THREAD] Завершение работы")
  sys.exit()
