import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)

class Door_sensors:
  def __init__(self, DOOR_UP_PIN=21, DOOR_DOWN_PIN=20, DOOR_BACK_PIN=5):
    self.DOOR_UP_PIN = DOOR_UP_PIN
    self.DOOR_DOWN_PIN = DOOR_DOWN_PIN
    self.DOOR_BACK_PIN = DOOR_BACK_PIN

    self.stop_function = lambda x : None
    
    GPIO.setup(self.DOOR_UP_PIN, GPIO.IN)
    GPIO.add_event_detect(self.DOOR_UP_PIN, GPIO.BOTH, callback=door_is_open)
    GPIO.setup(self.DOOR_DOWN_PIN, GPIO.IN)
    GPIO.add_event_detect(self.DOOR_DOWN_PIN, GPIO.BOTH, callback=door_is_open)
    GPIO.setup(self.DOOR_BACK_PIN, GPIO.IN)
    GPIO.add_event_detect(self.DOOR_BACK_PIN, GPIO.BOTH, callback=door_is_open)
    
  def door_is_open(self):
    print('[DOOR_SENSOR] Дверь открыта!')
    self.stop_function(-1)

def door_opened(channel):
  global up_door_state
  up_door_state = GPIO.input(DOOR_UP_PIN)



up_door_state = 0

GPIO.setup(DOOR_UP_PIN, GPIO.IN)
GPIO.add_event_detect(DOOR_UP_PIN, GPIO.BOTH, callback=door_opened)

while True:
  print("{}".format(up_door_state))


  time.sleep(0.05)
