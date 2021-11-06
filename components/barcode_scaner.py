import serial
import keyboard
import os


##class Scaner():
##  def __init__(self):
    
      

def read():
  with open("/dev/serial/by-id/usb-USBKey_Chip_USBKey_Module_202730041341-if00", 'r') as f:
    print('/ ', f.readline())
    yield f.readline()




if __name__ == '__main__':
  #scaner = Scaner()
  print('Reading')
  while True:
    print(read())
