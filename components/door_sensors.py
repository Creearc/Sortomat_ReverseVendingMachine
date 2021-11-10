import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)

class Door_sensors:
  def __init__(self, DOOR_UP_PIN = 2):
    self.DOOR_UP_PIN = DOOR_UP_PIN

    self.stop_function = lambda x : None
    
    GPIO.setup(self.DOOR_UP_PIN, GPIO.IN)
    GPIO.add_event_detect(self.DOOR_UP_PIN, GPIO.BOTH, callback=door_is_open)
    
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
