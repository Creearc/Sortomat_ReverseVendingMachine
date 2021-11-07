import time

states = {0 : lambda components, data : state_0(components, data),
          1 : lambda components, data : state_1(components, data),
          2 : lambda components, data : state_2(components, data),
          3 : lambda components, data : state_3(components, data),
          4 : lambda components, data : state_4(components, data),
          5 : lambda components, data : state_5(components, data),
          6 : lambda components, data : state_6(components, data),
          7 : lambda components, data : state_7(components, data),
          8 : lambda components, data : state_8(components, data),
          9 : lambda components, data : state_9(components, data),
           }

def state_0(components, data):
  t = time.time()
  components['rotator'].calibrate()
  while components['rotator'].working:
    if time.time() - t > components['ROTATOR_CALIBRATION_TIME']:
      return 0, -4

  return 1, 1 # Error code, next state

# 1 Покой
def state_1(components, data):
  if data['state_changed']:
    components['monitor'].state(1)
    components['light'].color_preset('blue')

  if data['points'] > 0:
    components['monitor'].set_points(data['points'], 0)
    components['monitor'].state(9)

  if components['ir_sensors'].is_hand():
    return 1, 2

  if time.time() - data['check_time'] > components['CHECK_TIME']:
    img = components['camera'].get_img()
    data['check_time'] = time.time()
    if components['camera'].is_object_blue(img, show=False, debug=False):
      return 1, 10
    else:
      components['weight'].set_null()

  is_critical, is_Full = components['us_sensor'].is_Full()
  if is_critical and is_Full:
    return 0, 12
  
  elif is_Full:
    return 1, 11
  
# 2 Рука  
def state_2(components, data): 
  if data['state_changed']:
    components['monitor'].state(2)
    components['light'].color_preset('blue')
    data['hand_detection_time'] = time.time()
  if not components['ir_sensors'].is_hand():
    return 1, 3
  if time.time() - data['hand_detection_time'] > components['HAND_DETECTION_TIME_LIMIT_SMALL']:
    return 1, 999
  
# 3 В крыльчатке может быть объект  
def state_3(components, data):
  time.sleep(0.2)
  if components['ir_sensors'].is_hand():
    return 1, 2
  img = components['camera'].get_img()
  if components['camera'].is_object_blue(img, show=False, debug=False):
    return 1, 4
  else:
    return 1, 13

# 4 Проверка веса 
def state_4(components, data):
  if components['ir_sensors'].is_hand():
    return 1, 2
  if components['weight'].is_heavy():
    return 1, 14
  return 1, 5

# 5 Распознавание объекта
def state_5(components, data):
  components['light'].color_preset('white', 100)
  time.sleep(0.2)
  if components['ir_sensors'].is_hand():
    return 1, 2
  for i in range(5):
    img = components['camera'].get_img()
  out = components['make_roi'](img)
  if out.shape == (0, 0, 3):
    out = img

  results = []
  results.append(components['nn_1'].classify_images([img[150:610, 80:1020]]))
  results.append(components['nn_1'].classify_images([out]))
  results.append(components['nn_2'].classify_images([out]))

  print(results)
  cv2.imwrite('{}/{}.png'.format(data['save_path'],
                                 len(os.listdir(data['save_path'])),
                                 ' '.join(results)), img)
  if results.count(components['SPECIAL']) == 3:
    data['add_points'] = 1
    components['rotator'].lert = False
    components['destroyer'].use = False
    return 1, 6
  if results.count('Other__Other2') == 0 and results.count('empty_Empty') == 0:
    data['add_points'] = 1
    components['rotator'].lert = True
    components['destroyer'].use = True
    return 1, 6
  return 1, 15

# 6 Запуск крыльчатки
def state_6(components, data):
  components['monitor'].state(3)
  components['light'].color_preset('green')
  components['rotator'].start()

  t = time.time()
  while components['rotator'].working:
    if components['ir_sensors'].is_hand():
      return 1, 16 
    if time.time() - t > components['ROTATOR_CALIBRATION_TIME']:
      return 1, 20
  return 1, 7 

# 7 Добавление баллов
def state_7(components, data):
  data['points'] += data['add_points']
  return 1, 8

# 8 Запуск сминателя
def state_8(components, data):
  if components['destroyer'].use == True:
    components['destroyer'].launch_destroyer()
    data['check_time'] = time.time()
  return 1, 1 

# 9 Запрос к сайту
def state_9(components, data):
  data['points'] = 0
  print(data['user_id'])
  return 1, 1 





if __name__ == '__main__':
  import sys
  path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
  sys.path.insert(0, path)
  import config.config as cf
  components = cf.components
  for key, value in states.items():
    try:
      value(components, None)
    except Exception as e:
      print(e)



















  
