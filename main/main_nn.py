# export DISPLAY=":0" && python3 main_0_2.py
import os
import sys
import RPi.GPIO as GPIO
from multiprocessing import Process, Value, Queue
import cv2
import threading
import time

import sys
path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
sys.path.insert(0, path)

from components import monitor
from components import light
from components import rotator
from components import ir_sensors
from components import destroyer
from components import weight
from components import camera

from components.neural_network import roi_function

#import data_creation_main as dcm

sys.path.insert(0, '{}/components/neural_network'.format(path))
from model_component import Model

model1 = Model("model_full_7classes_13may.tflite")
model1.debug = False
model1.input_shape = (512, 297, 3)
model1.labels = ['al__Other', 'empty_Empty', 'hdpe__ChemWhitemilk',
                 'Other__Other2', 'pet__Brown', 'pet__ChemOilMilk',
                 'pet__Green', 'pet__Transparent']

model2 = Model("model_roi_7classes_13may.tflite")
model2.debug = False
model2.input_shape = (448, 224, 3)
model2.labels = ['al__Other', 'empty_Empty', 'hdpe__ChemWhitemilk',
                 'Other__Other2', 'pet__Brown', 'pet__ChemOilMilk',
                 'pet__Green', 'pet__Transparent']

if not os.path.exists('data'):
  os.mkdir('data')

path = 'data/{}'.format(len(os.listdir('data')))
os.mkdir(path)

try:
  machine_state = 0
  machine_state_old = -1
  state_changed = False

  m = monitor.Monitor(1366, 768)
  m.start()
  m.state(0)

  print("_______________________________________________________________")
  print("Подготовка датчика веса")
  w = weight.Weight()
  print("Датчик веса готов")

  print("_______________________________________________________________")
  print("Подготовка камеры")
  c = camera.Camera()
  c.start()
  print("Камера готова")

  print("_______________________________________________________________")
  print("Подготовка освещения")
  l = light.Light()
  l.color_preset('blue')
  print("Освещение готово")

  print("_______________________________________________________________")
  print("Подготовка ИК датчиков")
  ir = ir_sensors.IR_sensors()
  print("ИК датчики готовы")

  print("_______________________________________________________________")
  print("Подготовка крыльчатки")
  r = rotator.Rotator()
  r.calibrate()
  print("Крыльчатка готова")

  print("_______________________________________________________________")
  print("Подготовка сминателя")
  s = destroyer.Destroyer()
  s.start()
  print("Сминатель готов")

  c_time = time.time()

  while True:
    state_changed = False
    if machine_state != machine_state_old:
      state_changed = True
    machine_state_old = machine_state

    # 0 Ожидание
    if machine_state == 0:
      if state_changed:
        m.state(1)
        l.color_preset('blue')      
      if time.time() - c_time > 1.5:
        img = c.get_img()    
        if camera.is_object_blue(img, show=False, debug=False):
          machine_state = -2
        else:
          machine_state = 0
          w.set_null()
        c_time = time.time()
      if ir.hand():
        machine_state = 1


    # -1 В отсеке лежит объект, который нужно забрать
    elif machine_state == -1:
      if state_changed:
        l.color_preset('red')
      img = c.get_img()      
      if not camera.is_object_red(img, show=False, debug=False):
        machine_state = 0
      if ir.hand():
        machine_state = 1
            
    # -2 В отсеке лежит объект, который нужно забрать
    elif machine_state == -2:
      if state_changed:
        m.state(5)
        l.color_preset('red')
      img = c.get_img()  
      if not camera.is_object_red(img, show=False, debug=False):
        machine_state = 0
      if ir.hand():
        machine_state = 1

    elif machine_state == -3:
      if state_changed:
        m.state(7)
        l.color_preset('red')
      img = c.get_img()      
      if not camera.is_object_red(img, show=False, debug=False):
        machine_state = 0
      if ir.hand():
        machine_state = 1

    # 1 В отсеке приема есть рука
    elif machine_state == 1:
      if state_changed:
        l.color_preset('blue')
        m.state(2)
      if not ir.hand():
        machine_state = 2


    # 2 В отсеке приема может находиться объект
    elif machine_state == 2:
      if ir.hand():
        machine_state = 1
      time.sleep(0.2)
      img = c.get_img()      
      if camera.is_object_blue(img, show=False, debug=False):
        machine_state = 3
      else:
        machine_state = 0

    # 3 В отсеке лежит объект
    elif machine_state == 3:
      if w.is_heavy():
        machine_state = -3
      else:
        machine_state = 4


    # 4 Ожидание ответа от распознавания
    elif machine_state == 4:
      if ir.hand():
        machine_state = 1
      else:
        l.color_preset('white', 100)
        time.sleep(0.2)
        for i in range(5):
          img = c.get_img()
        out = roi_function.roi(img)

        result_1 = model1.classify_images([img[150:610, 80:1020]])

        result_roi_1 = model1.classify_images([out])
        result_roi_2 = model2.classify_images([out])

        results = [result_1, result_roi_1, result_roi_2]
        print(results)
        
        if 'Other__Other2' in results or 'empty_Empty' in results :
          ai_answer = 1
        else:
          ai_answer = 0

        if results.count('al__Other') == 3:
          r.left = False
          s.use = False
        else:
          r.left = True
          s.use = True

        cv2.imwrite('{}/{} .png'.format(path, len(os.listdir(path)), ' '.join(results)), img)
        
        if ai_answer == 0:
          r.start()
          m.state(3)
          machine_state = 5
        else:
          m.state(4)
          machine_state = -1


    # 5 Вращение крыльчатки
    elif machine_state == 5:
      if state_changed:
        m.state(3) 
        l.color_preset('green')
      if not r.working:
        machine_state = 7
      if ir.hand():
        r.stop()
        machine_state = 6
      

    # 6 Остановка крыльчатки
    elif machine_state == 6:
      if state_changed:
        m.state(2) 
        l.color_preset('red')
      if not ir.hand():
        time.sleep(1.0)
        r.calibrate()
        machine_state = 5


    # 7 Включение сминателя
    elif machine_state == 7:
      if s.use == True:
        s.launch_destroyer()
        c_time = time.time()
      machine_state = 0

    if machine_state != machine_state_old:
      print("Состояние сортомата: {} ".format(machine_state))
      print("ИК датчики {} ".format(str(ir.hand())))
      print("Крыльчатка: {}".format(r.state))
      print("_______________________________________________________________")
    time.sleep(0.1)
      


except KeyboardInterrupt:
  GPIO.cleanup()
  print("_______________________________________________________________")
  print("Завершение работы")
  sys.exit()
