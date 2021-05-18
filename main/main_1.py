# export DISPLAY=":0" && python3 main_0_2.py
import os
import sys
path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
sys.path.insert(0, path)

import RPi.GPIO as GPIO
from multiprocessing import Process, Value, Queue
import cv2
import threading
import time

try:
  machine_state = 0
  machine_state_old = -1
  state_changed = False
  
  print("_______________________________________________________________")
  print("Подготовка монитора")
  from components import monitor
  m = monitor.Monitor(1366, 768)
  m.start()
  m.state(0)
  print("Монитор готов")

  print("_______________________________________________________________")
  print("Проверка лицензии")
  #from components import big_red_button
  print("Лицензия проверена")

  print("_______________________________________________________________")
  print("Подготовка датчика веса")
  from components import weight
  w = weight.Weight()
  print("Датчик веса готов")

  print("_______________________________________________________________")
  print("Подготовка освещения")
  from components import light
  l = light.Light()
  l.color_preset('blue')
  print("Освещение готово")

  print("_______________________________________________________________")
  print("Подготовка ИК датчиков")
  from components import ir_sensors
  ir = ir_sensors.IR_sensors()
  print("ИК датчики готовы")

  print("_______________________________________________________________")
  print("Подготовка крыльчатки")
  from components import rotator
  r = rotator.Rotator()
  r.calibrate()
  print("Крыльчатка готова")

  print("_______________________________________________________________")
  print("Подготовка сминателя")
  from components import destroyer
  s = destroyer.Destroyer()
  s.start()
  print("Сминатель готов")

  print("_______________________________________________________________")
  print("Подготовка камеры")
  from components import camera
  c = camera.Camera()
  c.start()
  print("Камера готова")

  print("_______________________________________________________________")
  print("Подготовка нейронных сетей")
  sys.path.insert(0, '{}/components/neural_network'.format(path))
  print(sys.path[0])
  import neural_network
  print(1)
  neural_network_component = neural_network.NeuralNetwork()
  print("Нейронные сети готовы")

  print("_______________________________________________________________")
  print("Подготовка модуля сохранения фото")
  sys.path.insert(0, path)
  from components import img_saver
  image_saver_component = img_saver.ImageSaver()
  sys.path.insert(0, '{}/test'.fomrat(path))
  print("Модуль сохранения фото готов")

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
          
        ai_answer, results = neural_network_component.run(img)
        image_saver_component.save(img, results)

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
      s.launch_destroyer()
      c_time = time.time()
      machine_state = 0

    if machine_state != machine_state_old:
      print('[System]')
      print('/////////////////////////////////////////////////////')
      print("Состояние сортомата: {} ".format(machine_state))
      print("ИК датчики {} ".format(str(ir.hand())))
      print("Крыльчатка: {}".format(r.state))
      print('/////////////////////////////////////////////////////')
    time.sleep(0.1)
      


except KeyboardInterrupt:
  GPIO.cleanup()
  print("_______________________________________________________________")
  print("Завершение работы")
  sys.exit()
