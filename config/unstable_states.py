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


def state_15(components, data):
  pass


def state_16(components, data):
  pass


def state_17(components, data):
  pass


def state_18(components, data):
  pass


def state_19(components, data):
  pass
