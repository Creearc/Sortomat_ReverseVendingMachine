import RPi.GPIO as GPIO
import sys
import os

##path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
##sys.path.insert(0, path)
path = sys.path[0].replace('\\', '/')
print(path)

print('[CONFIG] Начало')
components = dict()



components['ROTATOR_CALIBRATION_TIME'] = 3.0
components['CHECK_TIME'] = 1.5
components['FALSE_THINGS_COUNT'] = 5
components['HAND_DETECTION_TIME_LIMIT_SMALL'] = 10.0
components['HAND_DETECTION_TIME_LIMIT_BIG'] = 30.0
components['SAVE_PATH'] = 'data'
components['SPECIAL'] = 'al__Other'

print('[CONFIG] Сценариев')
from card_scaner.config import stable_states
from card_scaner.config import unstable_states
print('[CONFIG] Сценарии готовы')

print('[CONFIG] Загрузка компонента монитора')
os.environ['SDL_VIDEO_WINDOW_POS']='800,0'
from components import monitor
components['monitor'] = monitor.Monitor(400, 300, False)
components['monitor'].start()
components['monitor'].state(0)
print('[CONFIG] Монитор готов')

print('[CONFIG] Подготовка освещения')
from components import light
components['light'] = light.Light()
components['light'].color_preset('blue')
print('[CONFIG] Освещение готово')

print('[CONFIG] Загрузка нейронных сетей')
from components.neural_network import roi_function
components['make_roi'] = lambda img : roi_function.roi(img)

sys.path.insert(0, '{}/components/neural_network'.format(path))
from model_component import Model

components['nn_1'] = Model("{}/components/neural_network/models/model_full_7classes_13may.tflite".format(path))
components['nn_1'].debug = False
components['nn_1'].input_shape = (512, 297, 3)
components['nn_1'].labels = ['al__Other', 'empty_Empty', 'hdpe__ChemWhitemilk',
                 'Other__Other2', 'pet__Brown', 'pet__ChemOilMilk',
                 'pet__Green', 'pet__Transparent']

components['nn_2'] = Model("{}/components/neural_network/models/model_roi_7classes_13may.tflite".format(path))
components['nn_2'].debug = False
components['nn_2'].input_shape = (448, 224, 3)
components['nn_2'].labels = ['al__Other', 'empty_Empty', 'hdpe__ChemWhitemilk',
                 'Other__Other2', 'pet__Brown', 'pet__ChemOilMilk',
                 'pet__Green', 'pet__Transparent']


print('[CONFIG] Нейронные сети готовы')

print('[CONFIG] Подготовка крыльчатки')
from components import rotator
components['rotator'] = rotator.Rotator()
print('[CONFIG] Крыльчатка готова')

print('[CONFIG] Подготовка датчиков дверей')
from components import door_sensors       
components['door_sensors'] = door_sensors.Door_sensors()
print('[CONFIG] Датчики дверей готовы')

print('[CONFIG] Подготовка ИК датчиков')
from components import ir_sensors
components['ir_sensors']  = ir_sensors.IR_sensors()
print('[CONFIG] ИК датчики готовы')

print('[CONFIG] Подготовка УЗ датчика')
from components import us_sensors
components['us_sensor'] = us_sensors.US_sensor_Storage()
print('[CONFIG] УЗ датчик готов')

print('[CONFIG] Подготовка сминателя')
from components import destroyer
components['destroyer'] = destroyer.Destroyer()
components['destroyer'].start()
print('[CONFIG] Сминатель готов')

print('[CONFIG] Подготовка датчика веса')
##from components import weight
##components['weight'] = weight.Weight()
class Weight:
  def __init__(self):
    self.heavy = False
    self.delta = 0
  def is_heavy(self):
    return self.heavy
  def set_null(self):
    pass
  
components['weight'] = Weight()
print('[CONFIG] Датчик веса готов')


print('[CONFIG] Подготовка камеры')
from components import camera
components['camera'] = camera.Camera()
components['camera'].start()
print('[CONFIG] Камера готова')

print('[CONFIG] Подготовка сканера кодов')
from components import barcode_scaner
components['scaner'] = barcode_scaner.Scaner()
print('[CONFIG] Сканер кодов готов')















