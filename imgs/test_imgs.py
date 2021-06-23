import sys
import pygame
import cv2
import time

DARK_BLUE = (1.0 * 0x1b, 1.0 * 0x75, 1.0 * 0xbb)
LIGHT_BLUE = (1.0 * 0x00, 1.0 * 0xad, 1.0 * 0xef)
GREEN = (1.0 * 0xd6, 1.0 * 0xdf, 1.0 * 0x23)
WHITE = (255, 255, 255)

pygame.init()

def write(text, x, y, screen, color=(200, 200, 200), size=150, bold=True):
  font = pygame.font.SysFont("Arial", size, bold)
  text = font.render(str(text), 1, color)
  text_rect = text.get_rect(center=(x, y))
  screen.blit(text, text_rect)

class Monitor:
  def __init__(self, WIDTH=1920, HEIGHT=1080, full=True):
    self.WIDTH = WIDTH
    self.HEIGHT = HEIGHT

    if full:
      self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT],
                                            pygame.FULLSCREEN)
    else:
      self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
    self.clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    
    self.PATH = '/'.join(sys.path[0].replace('\\', '/').split('/'))
    self.img_state = 0
    self.timeout = 0
    self.points = 0

  # Цикл работы с монитором
  def monitor_process(self):
    IMG_START = self.load_image('start.png')
    IMG_READY = self.load_image('ready.png')
    IMG_HAND = self.load_image('leave_me_alone.png')
    IMG_BOTTLE = self.load_image('bottle.png')
    IMG_OTHER = self.load_image('other.png')
    IMG_CLEAN_IT = self.load_image('clean_it.png')
    IMG_SAVED = self.load_image('saved.png')
    IMG_WEIGHT = self.load_image('weight.png')
    IMG_QR = self.load_image('qr.png')
    IMG_POINTS = self.load_image('points.png')
    IMG_GENERATION = self.load_image('generation.png')
    imgs = [IMG_START, IMG_READY, IMG_HAND, IMG_BOTTLE,
            IMG_OTHER, IMG_CLEAN_IT, IMG_SAVED, IMG_WEIGHT,
            IMG_QR, IMG_POINTS, IMG_GENERATION ]
    self.img_state = 8
    self.points = -8
    self.timeout = 10
    while True:
      self.screen.fill((255, 255, 255))
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          break
      self.show_image(imgs[self.img_state])
      if self.points > 0:
        write(self.timeout, int(self.WIDTH // 1.7), int(self.HEIGHT * 0.73),
              self.screen,
              color=GREEN, size=130)
        
        write(self.points, int(self.WIDTH // 1.7), int(self.HEIGHT * 0.615),
              self.screen,
              color=LIGHT_BLUE, size=130)
        
      elif self.points < 0:
        self.show_image(self.load_image('tmp.png'))
        write(self.timeout, int(self.WIDTH // 1.7), int(self.HEIGHT * 0.648),
              self.screen,
              color=GREEN, size=130)
        
      pygame.display.flip()
      self.clock.tick(60)
      if not True:
        time.sleep(2.0)
        self.img_state += 1
        if self.img_state == len(imgs):
          self.img_state = 0
    pygame.quit()

  # Запуск монитора
  def start(self, left=True):
    print('Запущен монитор')
    self.process = Process(target=self.monitor_process, args=())
    self.process.start()

  # Остановка монитораs
  def stop(self):
    if self.process.is_alive():
      self.process.kill()

  def is_active(self):
    if self.process.is_alive():
      return True
    else:
      return False

  def state(self, s):
    self.img_state.value = s

  def set_points(self, p, t):
    self.points = p
    self.timeout = t

  # Загрузка изображения
  def load_image(self, path_to_img):
    img = pygame.image.load('{}/{}'.format(self.PATH, path_to_img))
    img = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
    rect = img.get_rect(bottomright=(self.WIDTH, self.HEIGHT))
    return [img, rect]

  # Отображение изображения
  def show_image(self, img):
    self.screen.blit(img[0], img[1])
    

if __name__ == '__main__':
  m = Monitor(full=False)
  m.monitor_process()
  