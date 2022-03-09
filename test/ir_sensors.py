# Модуль инфракрасных датчиков
import sys
import RPi.GPIO as GPIO
import threading
import time

GPIO.setmode(GPIO.BCM)

class IR_sensors:
  def __init__(self, PIN_1=6, PIN_2=12):
    # Пины
    self.PIN_1 = PIN_1
    GPIO.setup(self.PIN_1, GPIO.IN)
    GPIO.add_event_detect(self.PIN_1, GPIO.FALLING, callback=self.detect)

    self.PIN_2 = PIN_2
    GPIO.setup(self.PIN_2, GPIO.IN)
    GPIO.add_event_detect(self.PIN_2, GPIO.FALLING, callback=self.detect)


    # Переменные
    self.motion = False
    self.motion_delay = 1
    self.motion_time = time.time()

    self.lock = threading.Lock()

  def start(self):
    thrd = threading.Thread(target=self.process, args=())
    thrd.start()

  def process(self):
    while True:
      time.sleep(self.motion_delay)
      if time.time() - self.motion_time > self.motion_delay:
        with self.lock:
          self.motion = False


  # Изменение состояния датчика
  def detect(self, channel):
    self.motion = True

  def hand(self):
    return any([GPIO.input(self.PIN_1), GPIO.input(self.PIN_2)])

  def show_all(self):
    return [GPIO.input(self.PIN_1), GPIO.input(self.PIN_2)]


if __name__ == '__main__':
  import os
  try:
    os.environ['SDL_VIDEO_WINDOW_POS']='0,0'
    os.popen('DISPLAY=":0" lxterminal -e watch -n 0.1 -d tail -n 20 1.txt')
    ir = IR_sensors()
    while True:
      print(ir.hand())
      print(ir.show_all())
      f = open('1.txt', 'a')
      f.write('{}\n'.format(ir.show_all()))
      f.close()
      time.sleep(0.1)
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()

