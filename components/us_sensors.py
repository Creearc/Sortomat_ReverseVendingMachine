# Модуль ультразвуковых датчиков
import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class US_sensor:
  def __init__(self, TRIGGER_PIN, ECHO_PIN, measures_count):
    # Пины
    self.TRIGGER_PIN = TRIGGER_PIN
    self.ECHO_PIN = ECHO_PIN
    GPIO.setup(self.TRIGGER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(self.ECHO_PIN, GPIO.IN)
    
    # Переменные
    self.measures_count = measures_count
    self.distance = [11.0 for i in range(measures_count)]

  # Измерение расстояния при помощи УЗ датчика
  def measure(self):
    t = time.time()
    pulse_end_time, pulse_start_time = t, t
    GPIO.output(self.TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(self.TRIGGER_PIN, GPIO.LOW)

    while GPIO.input(self.ECHO_PIN)==0:
      pulse_start_time = time.time()
      if time.time() - t > 0.7:
        print('Не удалось измерить расстояние')
        return 11.0
    while GPIO.input(self.ECHO_PIN)==1:
      pulse_end_time = time.time()
      if time.time() - t > 0.7:
        print('Не удалось измерить расстояние')
        return 11.0

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    time.sleep(0.1)
    return distance

  def check_measure(self, d, k=0.1):
    for i in range(self.measures_count - 1, 0, -1):
      self.distance[i] = self.distance[i - 1]
    self.distance[0] = d
      
    
# Отсек приема
class US_sensor_Hand(US_sensor): 
  def __init__(self, TRIGGER_PIN=18, ECHO_PIN=14,
               HAND_DISTANCE=10, HAND_TIME_LIMIT=5.0,
               measures_count=2):
    super().__init__(TRIGGER_PIN, ECHO_PIN, measures_count)
    
    self.HAND_DISTANCE = HAND_DISTANCE
    self.HAND_TIME_LIMIT = HAND_TIME_LIMIT

    self.hand_state = False
   
  # Обнаружение руки
  def isHand(self):
    self.check_measure(self.measure())
    h = True
    nh = True
    for i in self.distance:
      if i > self.HAND_DISTANCE:
        h = False
      else:
        nh = False
    if h:
      self.hand_state = True
    if nh:
      self.hand_state = False
          
    if self.hand_state:
      return True
    else:
      return False

# Отсек приема
class US_sensor_Storage(US_sensor): 
  def __init__(self, TRIGGER_PIN=7, ECHO_PIN=15,
               FULL_DISTANCE=20, 
               measures_count=20):
    super().__init__(TRIGGER_PIN, ECHO_PIN, measures_count)

    self.FULL_DISTANCE = FULL_DISTANCE
    self.storage_state = False

  def isFull(self):
    self.check_measure(self.measure())
    f = True
    nf = True
    for i in self.distance:
      if i > self.FULL_DISTANCE:
        f = False
      else:
        nf = False
    if f:
      self.storage_state = True
    if nf:
      self.storage_state = False
          
    if self.storage_state:
      return True
    else:
      return False


if __name__ == '__main__':
  try:
    d1 = US_sensor_Storage()
    while True:
      print(d1.isFull())
      print(d1.distance)
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()  
