import threading
import os
import sys
path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
sys.path.insert(0, path)

test = not True
test_config = not True

if test_config:
  from config import config_test as config
else:
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
    
  def thread(self):
    while self.run:
      data['state_changed'] =  data['old_state'] != data['state']
      if data['state_changed']:
        print("[MAIN_THREAD] Состояние {}".format(data['state']))
        
      data['old_state'] = data['state']
      code, data['state'] = states[data['state']](components, data)
      if code == 0:
        data['error_code'] = data['state']
        break
      
    components['monitor'].state(0)
    print("[MAIN_THREAD] Ошибка номер {}".format(data['error_code']))
    

if __name__ == '__main__':
  try:
    if test:
      for key, value in states.items():
        print(key)
        try:
          value(components, data)
        except Exception as e:
          print(e)
    else:
      m = Main_thread()
      components['door_sensors'].stop_function = lambda x : m.stop(x)
      components['destroyer'].stop_function = lambda x : m.stop(x)
      m.start()

            
  except Exception as e:
    print("[MAIN_THREAD] {}".format(e))
    
  components['destroyer'].stop_destroyer()
  if not test_config:
    GPIO.cleanup() 
  print("_______________________________________________________________")
  print("[MAIN_THREAD] Завершение работы")
  sys.exit()
