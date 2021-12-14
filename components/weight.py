# Модуль датчика веса
import sys
import RPi.GPIO as GPIO
from multiprocessing import Process, Value
from hx711 import HX711
import time

GPIO.setmode(GPIO.BCM)


class Weight:
  def __init__(self, W_DOUT_PIN=25, W_CLK_PIN=8, HEAVY=23000):
    # Пины
    self.W_DOUT_PIN = W_DOUT_PIN
    self.W_CLK_PIN = W_CLK_PIN
    self.hx711 = HX711(
            dout_pin = self.W_DOUT_PIN,
            pd_sck_pin = self.W_CLK_PIN,
            channel='A',
            gain=64)
    self.hx711.reset()

    # Переменные
    self.HEAVY = HEAVY
    self.start_weight = 0
    self.delta = 0


  # Измерить вес
  def measure(self, t=2):
    m = self.hx711.get_raw_data(times=t)
    out = sorted(m)[len(m) // 2]
    return int(out)

  def set_null(self):
    self.start_weight = self.measure(5)

  def is_heavy(self):
    weight = self.measure(5)
    self.delta = weight - self.start_weight
    print(self.delta)
    if self.delta > self.HEAVY:
      return True
    else:
      return False     


if __name__ == '__main__':
  try:
    w = Weight()
    w.set_null()
    while True:
      print(w.is_heavy())
      
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()

