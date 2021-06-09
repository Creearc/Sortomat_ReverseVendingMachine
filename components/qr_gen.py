import cv2
import numpy as np
import requests
import qrcode
import json

DARK_BLUE = (1.0 * 0xbb, 1.0 * 0x75, 1.0 * 0x1b)
LIGHT_BLUE = (1.0 * 0xef, 1.0 * 0xad, 1.0 * 0x00)
GREEN = (1.0 * 0x23, 1.0 * 0xdf, 1.0 * 0xd6)
WHITE = (255, 255, 255)


def write(text, x, y, screen, color=(200, 200, 200), size=150):
  font = pygame.font.SysFont("Arial", size)
  text = font.render(text, 1, color)
  text_rect = text.get_rect(center=(x, y))
  screen.blit(text, text_rect)

def generate(points):
    baseUrl = 'http://lk.sortomat.ru'
    frontUrl = 'http://lk.sortomat.ru'
    credentials = {
        "email":'sortomat@sortomat.ru',
        "password":'<4>!k.Mn'
    }
    access_token = ''
    transaction_id = ''

    # get token
    try:
        r = requests.post(baseUrl+ '/api/auth/jwt/create', data=credentials)
        access_token = r.json()['access']
    except:
        pass


    if access_token:

        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }

        transaction_data = {
          "device":"00:1B:44:11:3A:B7",
          "amount":points
        }

        try:
            r = requests.post(baseUrl+ '/api/transactions/', data=json.dumps(transaction_data), headers=headers)
            print(r.content)
            transaction_id = r.json()['pk']
        except:
            pass


    if transaction_id:

        # Link for website
        input_data = frontUrl+'/points?id='+transaction_id+'&points={}'.format(points)

        # Creating an instance of qrcode
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
        qr.add_data(input_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save('qrcode.png')
        

def make_img(background, qr_name='qrcode.png'):
  img = cv2.imread(qr_name)
  out = cv2.imread(background)
  h, w = out.shape[:2]
  k = w // 4
  img = cv2.resize(img, (k, k))
  out[h // 2 - k // 2 + 20: h // 2 + k // 2 + 20,
      w // 2 - k // 2 : w // 2 + k // 2] = img
  
  return out


if __name__ == '__main__':
  import sys
  path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
  sys.path.insert(0, path)
  #generate(50)
  img = make_img('{}/imgs/qr.png'.format(path), '{}/qrcode.png'.format(path))
  
  cv2.imshow('', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()


