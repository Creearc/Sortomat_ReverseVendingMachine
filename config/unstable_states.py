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

def state_10(components, data):
  components['monitor'].state(5)
  components['light'].color_preset('red')
  data['false_things_counter'] += 1
  if data['false_things_counter'] >= components['FALSE_THINGS_COUNT']:
    return 0, -2
  if components['ir_sensors'].hand():
    return 1, 2
  img = components['camera'].get_img()
  if components['camera'].is_object_red(img, show=False, debug=False):
    return 1, 1


def state_11(components, data):
  components['light'].color_preset('red')
  print('БАК СКОРО ЗАПОЛНИТСЯ!')
  return 1, 1


def state_12(components, data):
  components['light'].color_preset('red')
  print('БАК ЗАПОЛНЕН!')
  return 0, 0


def state_13(components, data):
  components['monitor'].state(4)
  time.sleep(1.0)
  return 1, 1


def state_14(components, data):
  pass
