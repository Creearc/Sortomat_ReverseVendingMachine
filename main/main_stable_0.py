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
from components import qr_gen
from components import light
from components import rotator
from components import ir_sensors
from components import us_sensors
from components import destroyer
from components import weight
from components import camera

from components.neural_network import roi_function


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

save_path = 'data/{}'.format(len(os.listdir('data')))
os.mkdir(save_path)

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
  print("Подготовка УЗ датчика")
  us = us_sensors.US_sensor_Storage()
  print("УЗ датчик готов")

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
  C_TIME_PAUSE = 1.5

  hand_time = 0.0
  HAND_TIME_LIMIT_SMALL = 60.0 * 1
  HAND_TIME_LIMIT_LONG = 60.0 * 5

  special = 'al__Other'
  add_points = 0

  rotator_timer = 0.0
  ROTATOR_TIMER_LIMIT = 5.0
  
  points = 0
  points_timeout = 0
  POINTS_TIMEOUT_WAIT = 10
  POINTS_TIMEOUT_QR = 15

  while True:
    if machine_state != machine_state_old:
      state_changed = True
    machine_state_old = machine_state

    # 0 Покой
    if machine_state == 0:
      if state_changed:
        m.state(1)
        l.color_preset('blue')
  
      if ir.hand():
        machine_state = 1
      elif time.time() - c_time > C_TIME_PAUSE:
        img = c.get_img()
        c_time = time.time()
        if camera.is_object_blue(img, show=False, debug=False):
          machine_state = 11
        else:
          w.set_null()
      elif False:
        """Storage check"""
        pass
        
    # 1 Рука
    elif machine_state == 1:
      if state_changed:
        l.color_preset('blue')
        m.state(2)
        hand_time = time.time()
      if not ir.hand():
        machine_state = 2
      elif time.time() - hand_time > HAND_TIME_LIMIT_SMALL:
        machine_state = 12

    # 2 В крыльчатке может быть объект
    elif machine_state == 2:
      time.sleep(0.2)
      if ir.hand():
        machine_state = 1
      else:
        img = c.get_img()
        if camera.is_object_blue(img, show=False, debug=False):
          machine_state = 3
        else:
          machine_state = 13

    # 3 Проверка веса 
    elif machine_state == 3:
      if ir.hand():
        machine_state = 1
      elif w.is_heavy():
        machine_state = 14
      else:
        machine_state = 4

    # 4 Распознавание объекта
    elif machine_state == 4:
      l.color_preset('white', 100)
      time.sleep(0.2)
      if ir.hand():
        machine_state = 1
      else:
        for i in range(5):
          img = c.get_img()
        out = roi_function.roi(img)
        if out.shape == (0, 0, 3):
          out = img
          
        result_1 = model1.classify_images([img[150:610, 80:1020]])
        result_roi_1 = model1.classify_images([out])
        result_roi_2 = model2.classify_images([out])
        results = [result_1, result_roi_1, result_roi_2]

        print(results)
        cv2.imwrite('{}/{}.png'.format(save_path, len(os.listdir(save_path)), ' '.join(results)), img)

        if results.count(special) == 3:
          add_points = 1
          r.left = False
          s.use = False
          machine_state = 5
        elif results.count('Other__Other2') == 0 and results.count('empty_Empty') == 0:
          add_points = 1
          r.left = True
          s.use = True
          machine_state = 5
        else:
          machine_state = 15
        
    # 5 Запуск крыльчатки
    elif machine_state == 5:
      if state_changed:
        m.state(3) 
        l.color_preset('green')
        rotator_timer = time.time()
        r.start()
        
      if ir.hand():
        add_points = 0
        machine_state = 19
        
      if not r.working:
        machine_state = 6
      elif time.time() - rotator_timer > ROTATOR_TIMER_LIMIT:
        add_points = 0
        machine_state = 16
      
    # 6 Добавление баллов
    elif machine_state == 6:
      points += add_points
      machine_state = 7

    # 7 Запуск сминателя
    elif machine_state == 7:
      """Error 5"""
      if s.use == True:
        s.launch_destroyer()
        c_time = time.time()
      machine_state = 0

    # 0 Ожидание
    elif machine_state == 8:
      pass

    # 0 Ожидание
    elif machine_state == 9:
      pass

    # 0 Ожидание
    elif machine_state == 10:
      pass

    # 0 Ожидание
    elif machine_state == 11:
      pass

    # 0 Ожидание
    elif machine_state == 12:
      pass

    # 0 Ожидание
    elif machine_state == 13:
      pass

    # 0 Ожидание
    elif machine_state == 14:
      pass

    # 0 Ожидание
    elif machine_state == 15:
      pass

    # 0 Ожидание
    elif machine_state == 16:
      pass

    # 0 Ожидание
    elif machine_state == 17:
      pass

    # 0 Ожидание
    elif machine_state == 18:
      pass

    # 0 Ожидание
    elif machine_state == 19:
      pass

    # 0 Ожидание
    elif machine_state == 20:
      pass

    # 0 Ожидание
    elif machine_state == 21:
      pass

    # 0 Ожидание
    elif machine_state == 22:
      pass

    # 0 Ожидание
    elif machine_state == 23:
      pass

    # 0 Ожидание
    elif machine_state == 24:
      pass

    # 0 Ожидание
    elif machine_state == 25:
      pass

    # 0 Ожидание
    elif machine_state == 26:
      pass

    
    

    if machine_state != machine_state_old:
      print("Состояние сортомата: {} ".format(machine_state))
      print("ИК датчики {} ".format(str(ir.hand())))
      print("Крыльчатка: {}".format(r.state))
      print("_______________________________________________________________")
    time.sleep(0.1)
      


except KeyboardInterrupt:
  s.stop_destroyer()
  GPIO.cleanup()
  print("_______________________________________________________________")
  print("Завершение работы")
  sys.exit()
