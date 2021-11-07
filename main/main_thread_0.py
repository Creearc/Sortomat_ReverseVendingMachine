

import sys
path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
sys.path.insert(0, path)

from config import config

print('[MAIN_THREAD] Компоненты готовы')

components = config.components

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
