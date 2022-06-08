import time

states = {10 : lambda components, data : state_10(components, data),
          11 : lambda components, data : state_11(components, data),
          12 : lambda components, data : state_12(components, data),
          13 : lambda components, data : state_13(components, data),
          14 : lambda components, data : state_14(components, data),
          15 : lambda components, data : state_15(components, data),
          16 : lambda components, data : state_16(components, data),
          17 : lambda components, data : state_17(components, data),
          18 : lambda components, data : state_18(components, data),
          19 : lambda components, data : state_19(components, data),
          20 : lambda components, data : state_20(components, data),
          21 : lambda components, data : state_21(components, data),
          999 : lambda components, data : state_999(components, data),
           }

def state_999(components, data):
  if data['state_changed']:
    data['hand_detection_time'] = time.time()
    data['destroyer_state'] = components['destroyer'].direction
    components['destroyer'].stop_destroyer()
  if time.time() - data['hand_detection_time'] > components['HAND_DETECTION_TIME_LIMIT_BIG']:
    return 0, 1
  if not components['ir_sensors'].hand():
    if data['destroyer_state'] != 'off':
      components['destroyer'].launch_destroyer()      
    return 1, data['next_state']
  return 1, 999
  

def state_10(components, data):
  if data['state_changed']:
    components['monitor'].state(5)
    components['light'].color_preset('red')
    data['false_things_counter'] += 1
  if data['false_things_counter'] >= components['FALSE_THINGS_COUNT']:
    return 0, 2
  if components['ir_sensors'].hand():
    return 1, 2
  img = components['camera'].get_img()
  if not components['camera'].is_object_red(img, show=False, debug=False):
    return 1, 1
  return 1, 10


def state_11(components, data):
  components['light'].color_preset('red')
  print('БАК СКОРО ЗАПОЛНИТСЯ!')
  return 1, 1


def state_12(components, data):
  components['light'].color_preset('red')
  components['monitor'].state(11)
  return 0, 0


def state_13(components, data):
  components['monitor'].state(4)
  time.sleep(2.0)
  return 1, 1


def state_14(components, data):
  if data['state_changed']:
    components['monitor'].state(7)
    components['light'].color_preset('red')
  img = components['camera'].get_img()
  if not components['camera'].is_object_red(img, show=False, debug=False):
    return 1, 1    
  if components['ir_sensors'].hand():
    return 1, 2
  return 1, 14


def state_15(components, data):
  if data['state_changed']:
    components['monitor'].state(4)
    components['light'].color_preset('red')
  img = components['camera'].get_img()
  if not components['camera'].is_object_red(img, show=False, debug=False):
    return 1, 1 
  if components['ir_sensors'].hand():
    return 1, 2
  return 1, 15


def state_16(components, data):
  if data['state_changed']:
    components['monitor'].state(2)
    components['light'].color_preset('red')
    data['hand_detection_time'] = time.time()
  if time.time() - data['hand_detection_time'] > components['HAND_DETECTION_TIME_LIMIT_SMALL']:
    data['next_state'] = 17
    return 1, 999
  if not components['ir_sensors'].hand():
    return 1, 17
  return 1, 16


def state_17(components, data):
  if data['state_changed']:
    components['rotator'].left = not components['rotator'].left
    components['rotator'].start()
    data['check_time'] = time.time()

  if components['ir_sensors'].hand():
    components['rotator'].stop()
    return 1, 16 
  if time.time() - data['check_time'] > components['ROTATOR_CALIBRATION_TIME']:
    components['rotator'].stop()
    return 1, 18
  if not components['rotator'].working:
    return 1, 3
  return 1, 17


def state_18(components, data):
  if data['state_changed']:
    components['rotator'].left = not components['rotator'].left
    components['rotator'].start()
    data['check_time'] = time.time()
    
  if components['ir_sensors'].hand():
    components['rotator'].stop()
    return 1, 19 
  if time.time() - data['check_time'] > components['ROTATOR_CALIBRATION_TIME']:
    components['rotator'].stop()
    return 0, 4
  if not components['rotator'].working:
    return 1, 8
  return 1, 18


def state_19(components, data):
  if data['state_changed']:
    data['hand_detection_time'] = time.time()
  if time.time() - data['hand_detection_time'] > components['HAND_DETECTION_TIME_LIMIT_SMALL']:
    data['next_state'] = 18
    return 1, 999
  if not components['ir_sensors'].hand():
    return 1, 18
  return 1, 19


def state_20(components, data):
  if data['state_changed']:
    components['rotator'].left = not components['rotator'].left
    components['rotator'].start()
    data['check_time'] = time.time()

  if components['ir_sensors'].hand():
    components['rotator'].stop()
    return 1, 21
  if time.time() - data['check_time'] > components['ROTATOR_CALIBRATION_TIME']:
    components['rotator'].stop()
    return 0, 4
  if not components['rotator'].working:
    return 1, 3
  return 1, 20


def state_21(components, data):
  if data['state_changed']:
    data['hand_detection_time'] = time.time()
  if time.time() - data['hand_detection_time'] > components['HAND_DETECTION_TIME_LIMIT_SMALL']:
    data['next_state'] = 20
    return 1, 999
  if not components['ir_sensors'].hand():
    return 1, 20
  return 1, 21
