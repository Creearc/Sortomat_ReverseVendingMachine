# Модуль
import sys
import RPi.GPIO as GPIO
import threading
import time

GPIO.setmode(GPIO.BCM)

class Destroyer:
  def __init__(self, POWER_PIN=13, FORWARD_PIN=19, BACKWARD_PIN=26, SENSOR_PIN=27):
    # Пины
    self.POWER_PIN = POWER_PIN
    self.FORWARD_PIN = FORWARD_PIN
    self.BACKWARD_PIN = BACKWARD_PIN

    GPIO.setup(self.POWER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(self.FORWARD_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(self.BACKWARD_PIN, GPIO.OUT, initial=GPIO.LOW)

    # Оптический датчик
    self.SENSOR_PIN = SENSOR_PIN
    GPIO.setup(self.SENSOR_PIN, GPIO.IN)
    GPIO.add_event_detect(self.SENSOR_PIN,
                          GPIO.BOTH, callback=self.optical_sensor)

    # Переменные
    self.use = True
    self.step_time = 0
    self.reverse_time = 0
    self.working_time = 20
    self.reverse_working_time = 3

    self.end_time = time.time()

    self.command = 'off'
    self.direction = 'forward'

    self.lock = threading.Lock()

  def optical_sensor(self, channel):
    self.step_time = time.time()


  def stop(self):
    print('[Destroyer] Power OFF')
    GPIO.output(self.POWER_PIN, GPIO.LOW)
    time.sleep(1.0)
      
    print('[Destroyer] Directions OFF')
    GPIO.output(self.FORWARD_PIN, GPIO.LOW)
    GPIO.output(self.BACKWARD_PIN, GPIO.LOW)
    time.sleep(1.0)


  def forward(self):
    self.stop()

    print('[Destroyer] Forward')
    GPIO.output(self.FORWARD_PIN, GPIO.HIGH)
    time.sleep(1.0)
    
    self.direction = 'forward'
    self.step_time = time.time()
    GPIO.output(self.POWER_PIN, GPIO.HIGH)


  def backward(self):
    self.stop()
    
    print('[Destroyer] Backward')
    GPIO.output(self.BACKWARD_PIN, GPIO.HIGH)
    time.sleep(1.0)
    
    self.direction = 'backward'
    self.reverse_time = time.time()
    GPIO.output(self.POWER_PIN, GPIO.HIGH)

  
  def start(self):
    thrd = threading.Thread(target=self.process, args=())
    thrd.start()


  def process(self):
    with self.lock:
      self.command = 'wait'
    self.direction = 'off'
    while True:
      if self.command == 'forward':
        print('[Destroyer] Command -> Forward')
        self.forward()
        self.end_time = time.time() + self.working_time
        with self.lock:
            self.command = 'wait'

      elif self.command == 'backward':
        print('[Destroyer] Command -> Backward')
        self.backward()
        self.end_time = self.end_time + self.reverse_working_time
        with self.lock:
            self.command = 'wait'
            
      if self.direction == 'forward':
        if time.time() - self.step_time > 1:
          with self.lock:
            self.command = 'backward'
          print('[Destroyer] -> Low speed!')
        else:
          with self.lock:
            self.command = 'wait'
          
      elif self.direction == 'backward':
        if time.time() - self.reverse_time > self.reverse_working_time:
          with self.lock:
            self.command = 'forward'
          self.step_time = time.time()
          print('[Destroyer] -> Reverse finished!')
        else:
          with self.lock:
            self.command = 'wait'

      if (self.end_time - time.time() < 0 or self.direction == 'stop') and self.direction == 'forward':
        self.stop()
        self.direction = 'off'

      #print(self.command, self.direction)


  def launch_destroyer(self):
    with self.lock:
      if self.direction == 'off':
        self.command = 'forward'
      else:
        self.end_time = time.time() + self.working_time

  def stop_destroyer(self):
    with self.lock:
      self.command = 'stop'

if __name__ == '__main__':
  try:
    d = Destroyer()
    d.start()
    d.launch_destroyer()
  except KeyboardInterrupt:
    GPIO.output(self.POWER_PIN, GPIO.LOW)
    time.sleep(1.0)
    GPIO.cleanup()
    sys.exit()    
    
  
