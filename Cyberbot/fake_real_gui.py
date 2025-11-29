import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import tensorflow as tf
from tensorflow.keras.utils import img_to_array, load_img
import numpy as np
import os
import csv

# Load model once
model = tf.keras.models.load_model("fake_real_model.h5")

def predict_image(image_path):
    img = load_img(image_path, target_size=(128,128))
    img_array = img_to_array(img)/255.0
    img_array = np.expand_dims(img_array,0)
    pred = model.predict(img_array, verbose=0)[0][0]
    label = "Real" if pred>=0.5 else "Fake"
    confidence = pred if pred>=0.5 else 1-pred
    return label, confidence

def single_image_predict():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    label, conf = predict_image(file_path)
    messagebox.showinfo("Prediction", f"{label} ({conf:.2f})")

def batch_predict():
    folder = filedialog.askdirectory()
    if not folder:
        return
    results = []
    for subdir, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(subdir, file)
            label, conf = predict_image(path)
            results.append([path,label,round(conf,2)])
    output_csv = os.path.join(folder, "batch_predictions.csv")
    with open(output_csv,"w",newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Image","Prediction","Confidence"])
        writer.writerows(results)
    messagebox.showinfo("Batch Prediction", f"Done! Saved to {output_csv}")

def webcam_predict():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error","Cannot open camera")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img = cv2.resize(frame,(128,128))
        img_array = img_to_array(img)/255.0
        img_array = np.expand_dims(img_array,0)
        pred = model.predict(img_array, verbose=0)[0][0]
        label = "Real" if pred>=0.5 else "Fake"
        conf = pred if pred>=0.5 else 1-pred
        text = f"{label} ({conf:.2f})"
        cv2.putText(frame,text,(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.imshow("Webcam Prediction", frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# GUI
root = tk.Tk()
root.title("Fake vs Real Prediction")
root.geometry("300x200")

tk.Button(root, text="Single Image Predict", command=single_image_predict, width=25).pack(pady=10)
tk.Button(root, text="Batch Folder Predict", command=batch_predict, width=25).pack(pady=10)
tk.Button(root, text="Webcam Predict", command=webcam_predict, width=25).pack(pady=10)

root.mainloop()