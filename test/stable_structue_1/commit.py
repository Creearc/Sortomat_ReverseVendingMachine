# -*- coding: cp1251 -*-
from ftplib import FTP
import sys
fl = []
if len(sys.argv) > 1:
  for i in range(1, len(sys.argv)):
    print(sys.argv[i])
    fl.append(sys.argv[i])
else:
  fl.append('get_data.py')


for j in range(len(fl)):
  print(fl[j])

  ftp = FTP()
  HOSTS = ['10.11.0.2']
  PORT = 21
  for i in range(len(HOSTS)):
    ftp.connect(HOSTS[i], PORT)
    print(ftp.login(user='vasiliy', passwd='mushroom'))

    ftp.cwd('Project_folder')

    with open(fl[j], 'rb') as f:
        ftp.storbinary('STOR ' + fl[j].split('\\')[-1], f, 1024)

    print('Done!')
