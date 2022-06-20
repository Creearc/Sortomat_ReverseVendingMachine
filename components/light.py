# Модуль освещения
import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class Light:
  def __init__(self, BLUE_PIN=2, RED_PIN=3, GREEN_PIN=17, WHITE_PIN=4):
    ### Пины
    # Синий цвет
    self.BLUE_PIN = BLUE_PIN
    GPIO.setup(self.BLUE_PIN, GPIO.OUT, initial=GPIO.LOW)
    self.blue = GPIO.PWM(self.BLUE_PIN, 100)
    self.blue.start(0)
    self.blue_power = 100

    # Красный цвет
    self.RED_PIN = RED_PIN
    GPIO.setup(self.RED_PIN, GPIO.OUT, initial=GPIO.LOW)
    self.red = GPIO.PWM(self.RED_PIN, 100)
    self.red.start(0)
    self.red_power = 100

    # Зеленый цвет
    self.GREEN_PIN = GREEN_PIN
    GPIO.setup(self.GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
    self.green = GPIO.PWM(self.GREEN_PIN, 100)
    self.green.start(0)
    self.green_power = 100

    # Белый цвет
    self.WHITE_PIN = WHITE_PIN
    GPIO.setup(self.WHITE_PIN, GPIO.OUT, initial=GPIO.LOW)
    self.white = GPIO.PWM(self.WHITE_PIN, 100)
    self.white.start(0)
    self.white_power = 100

  # Яркость цвета
  def set(self, channel, p=0):
    if channel=='b':
      self.blue.ChangeDutyCycle(100 - p)
    elif channel=='r':
      self.red.ChangeDutyCycle(100 - p)
    elif channel=='g':
      self.green.ChangeDutyCycle(100 - p)
    elif channel=='w':
      self.white.ChangeDutyCycle(100 - p)

  # Цвет освещения
  def color(self, r, g, b, w):
    self.set('r', r)
    self.set('g', g)
    self.set('b', b)
    self.set('w', w)
  
  def color_preset(self, c='', p=None):
    if c == 'blue':
      if p is None:
        p = self.blue_power
      self.color(0, 0, p, 0)
    elif c == 'white':
      if p is None:
        p = self.white_power
      self.color(0, 0, 0, p)
    elif c == 'red':
      if p is None:
        p = self.red_power
      self.color(p, 0, 0, 0)
    elif c == 'yellow':
      if p is None:
        p = self.yellow_power
      self.color(p, p, 0, 0)
    elif c == 'green':
      if p is None:
        p = self.green_power
      self.color(0, p, 0, 0)
    elif c == 'all':
      if p is None:
        p = self.white_power
      self.color(p, p, p, p)
    else:
      self.color(0, 0, 0, 0)
    

#_________________________________________________________________________
if __name__ == '__main__':
  try:
    l = Light()
    while True:
      l.color_preset('red')
      time.sleep(2)
      l.color_preset('green')
      time.sleep(2)
      l.color_preset('blue')
      time.sleep(2)
      l.color_preset('white')
      time.sleep(2)
      l.color_preset('white', 20)
      time.sleep(2)
      l.color_preset('all')
      time.sleep(2)
      l.color_preset('off')
      time.sleep(2)

  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
    
