import requests
import threading
import sys
import time

SERVER_IP = 'http://18.222.180.114:8000'


def ask(url, parameter):
  url = '{}/get_{}'.format(url, parameter)
  response = requests.get(url=url)
  out = response.content
  return out

class Client:
  def __init__(self, IP='18.222.180.114', PORT=8000):
    self.IP = IP
    self.PORT = PORT
    self.state_to_num = {'normal' : 0, 'hand' : 1, 'bottle' : 5,  'not_bottle' : -1,
                         'heavy' : -3, 'no_hand' : 2, 'destroyer' : 7}
    self.lock = threading.Lock()

  def get_state(self):
    return self.state_to_num[self.state.decode()]

  def start(self):
    thrd = threading.Thread(target=self.process, args=())
    thrd.start()

  def process(self):
    while True:
      with self.lock:
        self.state = ask('http://{}:{}'.format(self.IP, self.PORT), 'state')
        self.manual = ask('http://{}:{}'.format(self.IP, self.PORT), 'manual') == b'True'
        self.aluminium = ask('http://{}:{}'.format(self.IP, self.PORT), 'aluminium') == b'True'
      #print(self.state, self.manual, self.aluminium)
      #print(self.get_state())
      time.sleep(0.01)


if __name__ == '__main__':
  try:
    c = Client()
    c.start()
  except KeyboardInterrupt:
    sys.exit()    
