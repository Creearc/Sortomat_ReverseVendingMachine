import RPi.GPIO as GPIO
import os
import sys
path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
sys.path.insert(0, path)

from config import config
components = config.components
print('[MAIN_THREAD] Компоненты готовы')

sys.path.insert(0, path)
from config import stable_states
from config import unstable_states

states = stable_states.states
states.update(unstable_states.states)

data = dict()
data['state'] = 0 
data['old_state'] = 0 
data['next_state'] = -1 
data['state_changed'] = False
data['check_time'] = 0 
data['false_things_counter'] = 0 
data['points'] = 0 
data['add_points'] = 0 
data['hand_detection_time'] = 0 
data['save_path'] = '{}/{}'.format(components['SAVE_PATH'],
                                   len(os.listdir(components['SAVE_PATH'])))
data['user_id'] = 0

test = True

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
      while True:
        data['state_changed'] =  data['old_state'] != data['state']
        data['old_state'] = data['state']
        code, data['state'] = states[data['state']](components, data)
        if code == 0:
          components['monitor'].state(0)
          print("[MAIN_THREAD] Ошибка номер {}".format(data['state']))
          break
        
  except KeyboardInterrupt:
    components['destroyer'].stop_destroyer()
    GPIO.cleanup()
    print("_______________________________________________________________")
    print("[MAIN_THREAD] Завершение работы")
    sys.exit()
