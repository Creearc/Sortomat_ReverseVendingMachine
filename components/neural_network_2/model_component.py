import numpy as np
import tensorflow as tf
import time
import cv2

"""
# MODEL:

IMG_SIZE = (320, 240)
IMG_SHAPE = IMG_SIZE + (3,)

BASE_MODEL = tf.keras.applications.VGG19(input_shape=IMG_SHAPE,
                                         include_top=False,
                                         weights='imagenet')
PREPROCESS_INPUT = tf.keras.applications.vgg19.preprocess_input

inputs = tf.keras.Input(shape=IMG_SHAPE)
x = PREPROCESS_INPUT(inputs)
x = BASE_MODEL(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.2)(x)
outputs = tf.keras.layers.Dense(1)(x)
model = tf.keras.Model(inputs, outputs)

model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  optimizer=tf.keras.optimizers.Adam(),
                  metrics=['accuracy'])
"""

class Model:
    def __init__(self, model_path="vgg19_17.h5"):
        self.classes = ['not_pet', 'pet']
        self.model = tf.keras.models.load_model(model_path)

    def run(self, path_to_image):
        image = tf.keras.preprocessing.image.load_img(path_to_image, target_size=(320, 240))

        image = tf.keras.preprocessing.image.img_to_array(image)
        image = np.expand_dims(image, axis=0)

        prediction_logit = self.model.predict_on_batch(image).flatten()
        prediction_sigmoid = tf.nn.sigmoid(prediction_logit)
        prediction = tf.where(prediction_sigmoid < 0.5, 0, 1)
        prediction = prediction.numpy()

        return self.classes[prediction[0]]
        

if __name__ == '__main__':

    classes = ['not_pet', 'pet']
    model = tf.keras.models.load_model("vgg19_17.h5")

    t = time.time()
    path_to_image = "A:/Projects/Sortomat_ReverseVendingMachine/dataset/pet__Milk+/2021_03_26/0_1_33075.png"
##    image = cv2.imread(path_to_image)
##    image = image.reshape(image.shape[1], image.shape[0], 3)
##    image = cv2.resize(image, (320, 240), interpolation = cv2.INTER_AREA)
##    
##    cv2.imshow('', image)
##    cv2.waitKey(0)
    image = tf.keras.preprocessing.image.load_img(path_to_image, target_size=(320, 240))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)

    prediction_logit = model.predict_on_batch(image).flatten()
    prediction_sigmoid = tf.nn.sigmoid(prediction_logit)
    prediction = tf.where(prediction_sigmoid < 0.5, 0, 1)
    prediction = prediction.numpy()
    print(time.time() - t)
    print(classes[prediction[0]])
