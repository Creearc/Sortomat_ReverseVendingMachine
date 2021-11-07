

import sys
path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
sys.path.insert(0, path)

from config import config

print('[MAIN_THREAD] Компоненты готовы')
