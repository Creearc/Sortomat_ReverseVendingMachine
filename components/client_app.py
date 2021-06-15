import requests
import threading

SERVER_IP = 'http://18.222.180.114:8000'


def ask(url, parameter):
  url = '{}/get_{}'.format(url, parameter)
  response = requests.get(url=url)
  out = response.content
  return out


print(ask(SERVER_IP, 'state'))
