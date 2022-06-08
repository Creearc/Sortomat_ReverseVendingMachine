import sys
import os

path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
sys.path.insert(0, path)
print(path)

components = dict()

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


while True:
    img = components['camera'].get_img()

    out = components['make_roi'](img)
    if out.shape == (0, 0, 3):
        out = img

    results = []
    results.append(components['nn_1'].classify_images([img[150:610, 80:1020]]))
    results.append(components['nn_1'].classify_images([out]))
    results.append(components['nn_2'].classify_images([out]))

    print('[STATE_5] results={}'.format(results))
    
