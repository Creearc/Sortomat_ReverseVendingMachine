from model import Model
import roi_function

class NeuralNetwork():
  def __init__(self):
    print('Model 1')
    model1 = Model("model_full_7classes_13may.tflite")
    print('Model 1 ready')
    model1.debug = False
    model1.input_shape = (512, 297, 3)
    model1.labels = ['al__Other', 'empty_Empty', 'hdpe__ChemWhitemilk',
                     'Other__Other2', 'pet__Brown', 'pet__ChemOilMilk',
                     'pet__Green', 'pet__Transparent']
    
    print('Model 2')
    model2 = Model("model_roi_7classes_13may.tflite")
    print('Model 2 ready')
    model2.debug = False
    model2.input_shape = (448, 224, 3)
    model2.labels = ['al__Other', 'empty_Empty', 'hdpe__ChemWhitemilk',
                     'Other__Other2', 'pet__Brown', 'pet__ChemOilMilk',
                     'pet__Green', 'pet__Transparent']
    
    self.models = [model1, model2]

  def run(self, img):
    roi_img = roi_function.roi(img)
    result = []
    result.append(self.models[0].classify_images([img[150:610, 80:1020]]))
    result.append(self.models[1].classify_images([roi_img]))
    result.append(self.models[2].classify_images([roi_img]))
    
    if 'Other__Other2' in results or 'empty_Empty' in results:
      ai_answer = 1
    else:
      ai_answer = 0
      
    return ai_answer, results
