

import sys
path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
sys.path.insert(0, path)

from config import config

print('[MAIN_THREAD] Компоненты готовы')

data = dict()
data['state']
data['old_state']
data['next_state']
data['state_changed']
data['check_time']
data['false_things_counter']
data['points']
data['add_points']
data['hand_detection_time']
data['save_path']
data['user_id']
