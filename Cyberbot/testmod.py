import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array


model = tf.keras.models.load_model("fake_real_model.h5")
print("Model loaded!")


img_path = "dataset/test/fake/fake1.jpg"
img = load_img(img_path, target_size=(128,128))
img_array = img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)


prediction = model.predict(img_array)[0][0]  
label = "Real" if prediction >= 0.5 else "Fake"
confidence = prediction if prediction >= 0.5 else 1 - prediction
print(f"Prediction: {label}, Confidence: {confidence:.2f}")
