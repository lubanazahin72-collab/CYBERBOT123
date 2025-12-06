import numpy as np
from PIL import Image
import tensorflow as tf  

tflite = tf.lite.Interpreter 

interpreter = tflite(model_path="model.tflite")
interpreter.allocate_tensors()


input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def predict_single_image(image):
    """
    image: can be a file path (str) or Django UploadedFile
    """
    # If it's a Django UploadedFile, read it
    if hasattr(image, 'read'):
        img = Image.open(image)
    else:
        img = Image.open(image)
    
    img = img.convert("RGB").resize((128, 128))  # adjust size as your model expects
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    label = int(np.argmax(output_data))
    confidence = float(np.max(output_data) * 100)  # percentage

    return {"label": label, "confidence": confidence, "id": None}


