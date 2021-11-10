import numpy as np
import sys
import tkinter as tk
import threading
import time
import os
##path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
##sys.path.insert(0, path)
path = sys.path[0].replace('\\', '/')
print(path)

print('[CONFIG] Начало')

components = dict()



components['ROTATOR_CALIBRATION_TIME'] = 10.0
components['CHECK_TIME'] = 1.5
components['FALSE_THINGS_COUNT'] = 5
components['HAND_DETECTION_TIME_LIMIT_SMALL'] = 10.0
components['HAND_DETECTION_TIME_LIMIT_BIG'] = 10.0
components['SAVE_PATH'] = 'data'
components['SPECIAL'] = 'al__Other'


print('[CONFIG] Загрузка компонента монитора')
class Monitor:
  def __init__(self, w, h):
    pass
  def start(self):
    pass
  def state(self, num):
    pass
  def set_points(self, num, p):
    pass
  
components['monitor'] = Monitor(1280, 1024)
components['monitor'].start()
components['monitor'].state(0)
print('[CONFIG] Монитор готов')

print('[CONFIG] Подготовка освещения')
class Light:
  def __init__(self):
    pass
  def color_preset(self, color, val=0):
    pass

  
components['light'] = Light()
components['light'].color_preset('blue')
print('[CONFIG] Освещение готово')

print('[CONFIG] Загрузка нейронных сетей')
from components.neural_network import roi_function
components['make_roi'] = lambda img : roi_function.roi(img)

class Model:
  def __init__(self, smth):
    self.debug = False
    self.input_shape = (512, 297, 3)
    self.labels = []
    self.out = 'pet__Transparent'
    
  def classify_images(self, img):
    return self.out

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
class Rotator:
  def __init__(self):
    self.left = True
    self.working = False
  def calibrate(self):
    self.working = True
  def start(self):
    self.working = True
  def stop(self):
    self.working = True
  
components['rotator'] = Rotator()
print('[CONFIG] Крыльчатка готова')


print('[CONFIG] Подготовка ИК датчиков')
class IR_sensors:
  def __init__(self):
    self.hand_var = True
  def hand(self):
    return self.hand_var 

    
components['ir_sensors']  = IR_sensors()
print('[CONFIG] ИК датчики готовы')

print('[CONFIG] Подготовка датчиков дверей')
class Door_sensors:
  def __init__(self):
    pass
  def start(self, t):
    thrd = threading.Thread(target=self.p, args=(t,))
    thrd.start()    
  def p(self, t):
    time.sleep(2)
    print('[DOOR_SENSOR] Дверь открыта!')
    t(-1)
        
components['door_sensors'] = Door_sensors()
print('[CONFIG] Датчики дверей готовы')

print('[CONFIG] Подготовка УЗ датчика')
class US_sensor_Storage:
  def __init__(self):
    self.full = False
    self.full_critical = False
  def is_Full(self):
    return self.full_critical, self.full
  
components['us_sensor'] = US_sensor_Storage()
print('[CONFIG] УЗ датчик готов')

print('[CONFIG] Подготовка сминателя')
class Destroyer:
  def __init__(self):
    self.use = False
    self.direction = 'forward'
  def start(self):
    pass
  def launch_destroyer(self):
    pass
  def stop_destroyer(self):
    pass
  
components['destroyer'] = Destroyer()
components['destroyer'].start()
print('[CONFIG] Сминатель готов')

print('[CONFIG] Подготовка датчика веса')
class Weight:
  def __init__(self):
    self.heavy = False
  def is_heavy(self):
    return self.heavy
  def set_null(self):
    pass
  
components['weight'] = Weight()
print('[CONFIG] Датчик веса готов')


print('[CONFIG] Подготовка камеры')
class Camera:
  def __init__(self):
    self.is_object = False
  def start(self):
    pass
  def get_img(self):
    return np.zeros((720, 1280, 3), np.uint8)
  def is_object_blue(self, img, show=False, debug=False):
    return self.is_object
  def is_object_red(self, img, show=False, debug=False):
    return self.is_object
  
components['camera'] = Camera()
components['camera'].start()
print('[CONFIG] Камера готова')

print('[CONFIG] Подготовка сканера кодов')
class Scaner:
  def __init__(self):
    self.heavy = False
    self.code = None
  def start(self):
    pass
  def get_code(self):
    return self.code
  
components['scaner'] = Scaner()
print('[CONFIG] Сканер кодов готов')





def button():
  global c, user_code, out_1, out_2
  components['ir_sensors'].hand_var = c[0].get()
  components['rotator'].working = not c[1].get()
  components['weight'].heavy = c[2].get()
  components['camera'].is_object = c[3].get() 
  components['us_sensor'].full = c[4].get()
  components['us_sensor'].full_critical = c[5].get()    

  if user_code.get() == 0:
    components['scaner'].code = None
  else:
    components['scaner'].code = user_code.get()

  components['nn_1'].out = out_1.get()
  components['nn_2'].out = out_2.get()


def interface():
  global c, user_code, out_1, out_2
  master = tk.Tk()
  master.title("Sortomat test")

  c = [tk.BooleanVar() for i in range(20)]

  tk.Button(master, text="Запуск", bg="white",
            width=200, height=3, command=button).grid(row=0, column=0)

  ch = ["Рука", "Датчик крыльчатки", "Тяжелый", "Объект", "Много бутылок", "Критично много"]

  for i in range(len(ch)):
    tk.Checkbutton(master, text=ch[i], variable=c[i],
                   onvalue=1, offvalue=0,
                   width=20, height=3).grid(row=(i+1), column=0)

  user_code = tk.IntVar()
  tk.Entry(master, textvariable=user_code).grid(row=len(ch)+1, column=0)
  out_1 = tk.StringVar()
  out_1.set('pet__Transparent')
  tk.Entry(master, textvariable=out_1).grid(row=len(ch)+1, column=1)
  out_2 = tk.StringVar()
  out_2.set('pet__Transparent')
  tk.Entry(master, textvariable=out_2).grid(row=len(ch)+1, column=2)

  master.mainloop()

c = []
user_code, out_1, out_2 = None, None, None

thrd = threading.Thread(target=interface, args=())
thrd.start()






