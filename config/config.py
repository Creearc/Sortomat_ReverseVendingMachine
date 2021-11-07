import RPi.GPIO as GPIO
import sys
##path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
##sys.path.insert(0, path)
path = sys.path[0].replace('\\', '/')
print(path)

print('[CONFIG] Начало')

GPIO.cleanup()
components = dict()






print('[CONFIG] Загрузка компонента монитора')
from components import monitor
#m = monitor.Monitor(1366, 768)
components['monitor'] = monitor.Monitor(1280, 1024)
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
components['weight'] = None#weight.Weight()
print('[CONFIG] Датчик веса готов')


print('[CONFIG] Подготовка камеры')
from components import camera
components['camera'] = camera.Camera()
components['camera'].start()
print('[CONFIG] Камера готова')

















