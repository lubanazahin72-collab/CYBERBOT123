import numpy as np
from PIL import Image
import tensorflow.lite as tflite
from io import BytesIO
import uuid

# Load TFLite model once
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def predict_single_image(image_file):
    """
    Predict a single image (from Django UploadedFile)
    Returns dict: label, confidence, id
    """
    # Read BytesIO
    image_file.seek(0)
    img_bytes = BytesIO(image_file.read())
    img = Image.open(img_bytes).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Set tensor and invoke
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    pred = float(output[0][0])

    label = "REAL" if pred > 0.5 else "FAKE"

    return {
        "label": label,
        "confidence": pred * 100,  # percentage
        "id": str(uuid.uuid4())[:8]
    }

