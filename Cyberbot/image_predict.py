import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

# মডেল লোড
model = tf.keras.models.load_model(r"E:\Desktop Backup\Documents\CYBERBOTDJANGO2.0\CYBERBOTDJANGO2\fake_real_model.h5")
print("Model loaded successfully!")

def predict_image(image_path):
    # Function-এর ভিতরের সব কোড indent করতে হবে
    img = load_img(image_path, target_size=(600,600))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, 0)
    prediction = model.predict(img_array, verbose=0)[0][0]
    label = "Real" if prediction >= 0.5 else "Fake"
    confidence = prediction if prediction >= 0.5 else 1 - prediction
    return label, confidence

def browse_and_predict():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        try:
            label, confidence = predict_image(file_path)
            messagebox.showinfo("Prediction", f"{file_path}\nPrediction: {label}\nConfidence: {confidence:.2f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

