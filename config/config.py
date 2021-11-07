import sys
##path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
##sys.path.insert(0, path)
path = sys.path[0].replace('\\', '/')
print(path)

print('[CONFIG] Начало')

components = dict()








print('[CONFIG] Загрузка нейронных сетей')
from components.neural_network import roi_function

sys.path.insert(0, '{}/components/neural_network'.format(path))
from model_component import Model

model1 = Model("{}/components/neural_network/model_full_7classes_13may.tflite".format(path))
model1.debug = False
model1.input_shape = (512, 297, 3)
model1.labels = ['al__Other', 'empty_Empty', 'hdpe__ChemWhitemilk',
                 'Other__Other2', 'pet__Brown', 'pet__ChemOilMilk',
                 'pet__Green', 'pet__Transparent']

model2 = Model("{}/components/neural_network/model_roi_7classes_13may.tflite".format(path))
model2.debug = False
model2.input_shape = (448, 224, 3)
model2.labels = ['al__Other', 'empty_Empty', 'hdpe__ChemWhitemilk',
                 'Other__Other2', 'pet__Brown', 'pet__ChemOilMilk',
                 'pet__Green', 'pet__Transparent']


print('[CONFIG] Нейронные сети готовы')

print('[CONFIG] Загрузка компонента монитора')
from components import monitor
m = monitor.Monitor(1366, 768)
m.start()
m.state(0)
print('[CONFIG] Монитор готов')

print('[CONFIG] Подготовка освещения')
from components import light
l = light.Light()
l.color_preset('blue')
print('[CONFIG] Освещение готово')

print('[CONFIG] Подготовка крыльчатки')
from components import rotator
r = rotator.Rotator()
r.calibrate()
print('[CONFIG] Крыльчатка готова')


print('[CONFIG] Подготовка ИК датчиков')
from components import ir_sensors
ir = ir_sensors.IR_sensors()
print('[CONFIG] ИК датчики готовы')


print('[CONFIG] Подготовка УЗ датчика')
from components import us_sensors
us = us_sensors.US_sensor_Storage()
print('[CONFIG] УЗ датчик готов')

print('[CONFIG] Подготовка сминателя')
from components import destroyer
s = destroyer.Destroyer()
s.start()
print('[CONFIG] Сминатель готов')

print('[CONFIG] Подготовка датчика веса')
from components import weight
w = weight.Weight()
print('[CONFIG] Датчик веса готов')


print('[CONFIG] Подготовка камеры')
from components import camera
c = camera.Camera()
c.start()
print('[CONFIG] Камера готова')

















