import numpy as np
from PIL import Image
import tensorflow as tf

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Class names
CLASSES = ["FAKE", "REAL"]

def predict_single_image(image):
    """
    image: file path (str) or Django UploadedFile
    Returns: dict with label, confidence, and id
    """
    # Open image
    if hasattr(image, 'read'):
        img = Image.open(image)
    else:
        img = Image.open(image)

    # Resize to model input
    img = img.convert("RGB").resize((224, 224))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    label_index = int(np.argmax(output_data))
    label = CLASSES[label_index]
    confidence = float(np.max(output_data) * 100)

    return {"label": label, "confidence": confidence, "id": None}

    

