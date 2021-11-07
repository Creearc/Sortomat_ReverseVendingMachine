
import os
import sys
path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
sys.path.insert(0, path)

from config import config
components = config.components
print('[MAIN_THREAD] Компоненты готовы')

sys.path.insert(0, path)
from config import stable_states

states = stable_states.states

data = dict()
data['state'] = 0 
data['old_state'] = 0 
data['next_state'] = 0 
data['state_changed'] = False
data['check_time'] = 0 
data['false_things_counter'] = 0 
data['points'] = 0 
data['add_points'] = 0 
data['hand_detection_time'] = 0 
data['save_path'] = '{}/{}'.format(components['SAVE_PATH'],
                                   len(os.listdir(components['SAVE_PATH'])))
data['user_id'] = 0



if __name__ == '__main__':
  for key, value in states.items():
    print(key)
    try:
      value(components, data)
    except Exception as e:
      print(e)
