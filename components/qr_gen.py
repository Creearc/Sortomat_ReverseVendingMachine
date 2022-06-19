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

def generate(points, save_path):
    baseUrl = 'https://sortomat-api.herokuapp.com'
    frontUrl = 'https://sortomat-app.herokuapp.com'
    credentials = {
        "email":'sortomat@sortomat.ru',
        "password":'<4>!k.Mn'
    }
    access_token = ''
    transaction_id = ''

    # get token
    try:
        r = requests.post(baseUrl + '/api/jwt/create', data=credentials)
        access_token = r.json()['access']
    except Exception as e:
            print('Exception 1 ', e)


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
            print('content', r.content)
            transaction_id = r.json()['pk']
        except Exception as e:
            print('Exception 2 ', e)

    print('transaction_id', transaction_id)
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
        img.save(save_path)
        

def make_img(background, save_path, qr_name='qrcode.png'):
  img = cv2.imread(qr_name)
  #img = img[40 : 430,  40 : 430].copy()
  out = cv2.imread(background)
  h, w = out.shape[:2]
  k = w // 6
  img = cv2.resize(img, (k, k))
  center = int(w // 5.335), int(h // 2)
  out[center[1] - k // 2: center[1] + k // 2,
      center[0] - k // 2 : center[0] + k // 2] = img
  cv2.imwrite('{}/tmp.png'.format(save_path), out)
  return out


if __name__ == '__main__':
  import sys
  path = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])
  sys.path.insert(0, path)
  print(path)
  generate(58, '{}/qrcode.png'.format(path))
  img = make_img('{}/imgs/qr.png'.format(path),
                 '{}/imgs'.format(path),
                 '{}/qrcode.png'.format(path))
  
  cv2.imshow('', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()


