import RPi.GPIO as GPIO
import sys
import os
##path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
##sys.path.insert(0, path)
path = sys.path[0].replace('\\', '/')
print(path)

print('[CONFIG] Начало')
components = dict()

print('[CONFIG] Сценариев')
from config.qr_1 import stable_states
from config.qr_1 import unstable_states
print('[CONFIG] Сценарии готовы')

components['ROTATOR_CALIBRATION_TIME'] = 3.0
components['CHECK_TIME'] = 1.5
components['FALSE_THINGS_COUNT'] = 5
components['HAND_DETECTION_TIME_LIMIT_SMALL'] = 10.0
components['HAND_DETECTION_TIME_LIMIT_BIG'] = 30.0
components['SAVE_PATH'] = 'data'
components['SPECIAL'] = 'al__Other'


print('[CONFIG] Загрузка компонента монитора')
from components import monitor
components['monitor'] = monitor.Monitor(1366, 768)
components['monitor'].start()
components['monitor'].state(0)
print('[CONFIG] Монитор готов')

print('[CONFIG] Подготовка освещения')
from components import light
components['light'] = light.Light(BLUE_PIN=2, RED_PIN=3, GREEN_PIN=4, WHITE_PIN=17)
components['light'].color_preset('blue')
print('[CONFIG] Освещение готово')

print('[CONFIG] Загрузка нейронных сетей')
from components.neural_network import roi_function
components['make_roi'] = lambda img : roi_function.roi(img)

sys.path.insert(0, '{}/components/neural_network_2'.format(path))
from model_component import Model

components['nn_1'] = Model("vgg19_17.h5".format(path))
print('[CONFIG] Нейронные сети готовы')

print('[CONFIG] Подготовка крыльчатки')
from components import rotator
components['rotator'] = rotator.Rotator()
print('[CONFIG] Крыльчатка готова')

print('[CONFIG] Подготовка датчиков дверей')
from components import door_sensors_old as door_sensors   
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
from components import weight
components['weight'] = weight.Weight() 
print('[CONFIG] Датчик веса готов')


print('[CONFIG] Подготовка камеры')
from components import camera
components['camera'] = camera.Camera()
components['camera'].start()
components['camera'].red_region = [100, 520, 200, 980]
components['camera'].red_gamma = 7.5
components['camera'].red_max = 10

components['camera'].blue_region = [120, 520, 200, 980]
components['camera'].blue_gamma = 4.5
components['camera'].blue_max = 10
print('[CONFIG] Камера готова')

print('[CONFIG] Подготовка сканера кодов')
from components import barcode_scaner
components['scaner'] = barcode_scaner.Scaner()
print('[CONFIG] Сканер кодов готов')















