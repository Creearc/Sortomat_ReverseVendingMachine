import serial
import keyboard
import os


class Scaner():
  def __init__(self, device='/dev/hidraw0', bandwidth=9600):
    self.ser = serial.Serial(device, bandwidth)

def read():
  out = ''
  while out == '':
    out = os.popen("cat /dev/serial/by-id/usb-USBKey_Chip_USBKey_Module_202730041341-if00").read()
  return out




if __name__ == '__main__':
  #scaner = Scaner()
  print('Reading')
  while True:
    print(read())
##   while True:
##     print(keyboard.read_key())
