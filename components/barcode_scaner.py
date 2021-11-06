def read():
  out = ''
  last = 0
  counter = 0 
  with open('/dev/usb/hiddev0', 'rb') as f:
    while True:
      tmp = f.read(8)
      try:
        tmp = tmp[3:].decode()[1]
        out = '{}{}'.format(out, tmp)
      except:
        print('[BARCODE_SCANER] Unsupported code')
        return None
  
      if ord(tmp) == 125 and last == 34:
        break
      else:
        last = ord(tmp)
      counter += 1
    return out.split('data')[-1][3:-2]
  




if __name__ == '__main__':
  print('Reading')
  while True:
    print(read())
