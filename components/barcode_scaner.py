import serial

class Scaner():
  def __init__(self, device='/dev/serial0', bandwidth=9600):
    self.ser = serial.Serial(device, bandwidth)

  def read(self):
    s = b''
    while s == b'':
      s = self.ser.readline()
    return int(s.decode())

  def tell(self, command):
    self.ser.write('{}\n'.format(command).encode())



if __name__ == '__main__':
##  scaner = Scaner()
##  print('Reading')
##  while True:
##    print(scaner.read())
  while True:
    print(input())
