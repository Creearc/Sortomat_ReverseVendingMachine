# Модуль крыльчатки
import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class Rotator:
  def __init__(self, STEP_PIN=24, DIR_PIN=22,
               ROTATOR_OPTICAL_PIN=16):

    ### Пины
    # Шаговый двигатель
    self.STEP_PIN = STEP_PIN
    self.DIR_PIN = DIR_PIN
    GPIO.setup(self.STEP_PIN, GPIO.OUT)
    GPIO.setup(self.DIR_PIN, GPIO.OUT)
    self.process = GPIO.PWM(STEP_PIN, 1)
   
    # Оптический датчик
    self.ROTATOR_OPTICAL_PIN = ROTATOR_OPTICAL_PIN
    GPIO.setup(self.ROTATOR_OPTICAL_PIN, GPIO.IN)
    GPIO.add_event_detect(self.ROTATOR_OPTICAL_PIN,
                          GPIO.BOTH, callback=self.optical_sensor)

    ### Переменные
    # Шаговый двигатель
    self.frequency = 500
    self.left = True
    self.working = False
    
    # Оптический датчик
    self.use_opical_sensor = True
    self.state = 0
    self.old_state = 0
    self.wait = True

  # Калибровка крыльчатки
  def calibrate(self):
    if GPIO.input(self.ROTATOR_OPTICAL_PIN) == 1:
      print('[ROTATOR] Калибровка крыльчатки')
      if self.left:
        GPIO.output(self.DIR_PIN, GPIO.LOW)
      else:
        GPIO.output(self.DIR_PIN, GPIO.HIGH)   
      self.process.start(50)
      self.process.ChangeFrequency(self.frequency)
      self.working = True
      self.wait = False

  # Запуск крыльчатки
  def start(self):
    print('[ROTATOR] Крыльчатка запущена')
    if self.left:
      GPIO.output(self.DIR_PIN, GPIO.LOW)
    else:
      GPIO.output(self.DIR_PIN, GPIO.HIGH)
    self.process.start(50)
    self.process.ChangeFrequency(self.frequency)
    
    self.working = True
    self.wait = True
    time.sleep(0.1)
    self.wait = False

  # Остановка крыльчатки
  def stop(self):
    self.process.stop()
    self.working = False
    print('[ROTATOR] Крыльчатка остановлена')

  # Оптический датчик
  def optical_sensor(self, channel):
    self.old_state = self.state
    self.state = GPIO.input(self.ROTATOR_OPTICAL_PIN)
    if self.old_state == 1 and self.state == 0 and self.use_opical_sensor and not self.wait:
      self.stop()
      time.sleep(0.2)
      self.old_state = 0


if __name__ == '__main__':
  try:
    r = Rotator()
    r.start()
    while True:
      
      time.sleep(3.0)
      #r.stop()
        
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()

