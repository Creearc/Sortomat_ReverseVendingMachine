import numpy as np
import cv2

def hamming(a, b):
  return bin(int(a) ^ int(b)).count("1")

def dhash(img, hashSize=3):
  img = cv2.resize(img, (hashSize, img.shape[0]))
  img = cv2.blur(img, (3, 3))
  diff = img[:, 1:] > img[:, :-1]
  return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


class Glue:
    def __init__(self, region):
        self.region = region

        self.region_w = region[1][0] - region[0][0]
        self.region_h = region[1][1] - region[0][1]

        self.step = 10
        self.hash_size = 100

        self.reset()

    def run(self, img):
        part = img[self.region[0][1] : self.region[1][1],
                   self.region[0][0] : self.region[1][0]]

        mn, ind = -1, 0
        if not(self.d0 is None):
            for i in range(part.shape[0] // self.step):
                d = dhash(part[i * self.step : (i + 1) * self.step, : ], hashSize=self.hash_size)
                ham = hamming(d, self.d0)
                if mn == -1 or mn > ham:
                    mn = ham
                    ind = i

            #print(mn, ind, H)
            if ind >= int(self.step * 0.8):
                return self.result
            #print(ind, part.shape[0] // self.step)
            disp = part.shape[0] - ind * self.step
            try:
              self.result[self.pos - self.step : self.pos - self.step + (part.shape[0] - ind * self.step),
                  :] = part[ind * self.step : , :]
            except:
              self.reset()
        else:
            disp = part.shape[0]
            self.result[0 : part.shape[0], 0 : part.shape[1]] = part[:,:]

        self.d0 = dhash(part[-self.step : -1, : ], hashSize=self.hash_size)
        self.pos += disp
        if self.pos + part.shape[0] > self.result.shape[0]:
            self.pos = 0
            
        return self.result

    def reset(self):
        self.d0 = None
        self.pos = 0        
        self.result = np.zeros((self.region_h * 8, self.region_w, 3), np.uint8)



if __name__ == "__main__":
    WEIGHT, HIGHT = 1920, 1080
    
    g = Glue([(int(WEIGHT * 0.14), int(HIGHT * 0.47)),
              (int(WEIGHT * 0.97), int(HIGHT * 0.82))])

    print(g.pos)
