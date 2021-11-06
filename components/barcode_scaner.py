import serial
import keyboard
import os


class Scaner():
  def __init__(self, device='/dev/hidraw0', bandwidth=9600):
    self.ser = serial.Serial(device, bandwidth)

def read():
  with open("/dev/serial/by-id/usb-USBKey_Chip_USBKey_Module_202730041341-if00", 'r') as f:
    out = f.readlines()
  return out




if __name__ == '__main__':
  #scaner = Scaner()
  print('Reading')
  while True:
    print(read())
