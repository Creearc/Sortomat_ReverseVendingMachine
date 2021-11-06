import serial
import keyboard
import os
import time()


##class Scaner():
##  def __init__(self):
    
      

def read():
  with open("/dev/serial/by-id/usb-USBKey_Chip_USBKey_Module_202730041341-if00", 'r') as f:
    while True:
      try:
        out = f.readline()
        print('? ', out)
      except:
        print('________')
        break
    return out




if __name__ == '__main__':
  #scaner = Scaner()
  time.sleep(2.0)
  print('Reading')
  while True:
    print(read())
