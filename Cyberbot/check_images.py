import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np

model = tf.keras.models.load_model("fake_real_model.h5")

def predict_image(image_path):
    img = load_img(image_path, target_size=(128,128))
    img_array = img_to_array(img)/255.0
    img_array = np.expand_dims(img_array, 0)
    
    pred = model.predict(img_array, verbose=0)[0]  # shape: (2,)
    label_index = np.argmax(pred)  # 0 = Fake, 1 = Real
    label = "Fake" if label_index == 0 else "Real"
    confidence = pred[label_index]
    
    return label, round(confidence, 2)

# Example usage
label, conf = predict_image("dataset/test/fake/fake1.jpg")
print(f"Prediction: {label}, Confidence: {conf}")
