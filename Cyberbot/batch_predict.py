import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import os
import cv2
import csv

# ---------------- Load model ----------------
model = tf.keras.models.load_model("fake_real_model.h5")
print("Model loaded successfully!")

# ---------------- Prediction Function ----------------
def predict_image(image_path):
    """
    Predict label and confidence for a single image.
    Works for models with 2-output softmax.
    """
    # Load image and convert to RGB
    img = load_img(image_path, target_size=(128,128))
    img_array = img_to_array(img.convert("RGB")) / 255.0  # normalize
    img_array = np.expand_dims(img_array, axis=0)  # add batch dim

    pred = model.predict(img_array, verbose=0)[0]  # shape (2,)
    label_index = np.argmax(pred)  # 0 = Fake, 1 = Real
    label = "Fake" if label_index == 0 else "Real"
    confidence = pred[label_index]

    return label, round(confidence,2)

# ---------------- Batch Prediction ----------------
def batch_predict(folder_path="dataset/test", output_csv="predictions.csv"):
    results = []

    for subdir, _, files in os.walk(folder_path):
        for file in files:
            image_path = os.path.join(subdir, file)
            try:
                label, confidence = predict_image(image_path)
                results.append([image_path, label, confidence])
                print(f"{image_path} --> {label} ({confidence:.2f})")
            except Exception as e:
                print(f"Skipping {image_path}: {e}")

    # Save results to CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Image", "Prediction", "Confidence"])
        writer.writerows(results)

    print(f"\nBatch prediction done! Results saved to {output_csv}")

# ---------------- Webcam Prediction ----------------
def webcam_predict():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert BGR to RGB
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img, (128,128))
        img_array = img_to_array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        pred = model.predict(img_array, verbose=0)[0]
        label_index = np.argmax(pred)
        label = "Fake" if label_index == 0 else "Real"
        confidence = pred[label_index]

        text = f"{label} ({confidence:.2f})"
        cv2.putText(frame, text, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.imshow("Webcam Prediction", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Single image test
    img_path = "dataset/test/fake/fake1.jpg"
    label, conf = predict_image(img_path)
    print(f"Single Image -> {img_path} : {label} ({conf:.2f})")

