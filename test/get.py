# -*- coding: cp1251 -*-
from ftplib import FTP
import sys

PATH = '\\'.join(sys.argv[0].split('\\')[:-1])

ftp = FTP()
HOST = '192.168.137.189'
#HOST = '192.168.137.164'
PORT = 21

ftp.connect(HOST, PORT)

print(ftp.login(user='pi', passwd='9'))


ftp.cwd('~/main3/data')


#for i in range(28, 36):
if True:
  i = 'dataset_14052021'
  fl = '{}.zip'.format(i)
  out = '{}\{}'.format(PATH, fl)

  with open(out, 'wb') as f:
      ftp.retrbinary('RETR ' + fl, f.write)

