
import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np

# Load model only once
model = tf.keras.models.load_model(r"fake_real_model.h5")

def predict_image(image_path):
    img = load_img(image_path, target_size=(600,600))
    img_array = img_to_array(img)/255.0
    img_array = np.expand_dims(img_array,0)
    pred = model.predict(img_array, verbose=0)[0][0]
    label = "Real" if pred>=0.5 else "Fake"
    confidence = pred if pred>=0.5 else 1-pred
    return label, round(confidence,2)



