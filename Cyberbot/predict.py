import numpy as np
from PIL import Image
import tensorflow as tf

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Detect model input shape automatically
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Model expected dimensions
MODEL_H = input_details[0]['shape'][1]
MODEL_W = input_details[0]['shape'][2]

def predict_single_image(image):
    """Predict any image of any size for correct model output"""

    # Load image safely
    if hasattr(image, 'read'):
        img = Image.open(image)
    else:
        img = Image.open(image)

    # Ensure RGB (for models trained on 3 channels)
    img = img.convert("RGB")

    # Resize to EXACT model-required size
    img = img.resize((MODEL_W, MODEL_H))

    # Convert to array
    img_array = np.array(img, dtype=np.float32)

    # Normalize (0–255 → 0–1) if model trained that way
    img_array = img_array / 255.0

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    # Feed into model
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()

    # Get output
    output = interpreter.get_tensor(output_details[0]['index'])

    # Predicted label + confidence
    label = int(np.argmax(output))
    confidence = float(np.max(output) * 100)

    return {
        "label": label,
        "confidence": confidence,
        "model_input_shape": f"{MODEL_W}x{MODEL_H}"
    }

