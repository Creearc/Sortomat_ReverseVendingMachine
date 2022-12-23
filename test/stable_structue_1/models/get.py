# -*- coding: cp1251 -*-
import threading
from ftplib import FTP
import sys

PATH = '\\'.join(sys.argv[0].split('\\')[:-1])

def main_thread():
  ftp = FTP()
  HOST = '192.168.0.105'
  PORT = 21

  ftp.connect(HOST, PORT)

  print(ftp.login(user='alexandr', passwd='9'))

  ftp.cwd('yolov5/runs/train/sortomat_s_736_0/weights')

  for i in ['best.pt']:
    try:
      with open(i, 'wb') as f:
        ftp.retrbinary('RETR ' + i, f.write)
    except:
      print(i)


main_thread()
