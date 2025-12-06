import tensorflow as tf

# Load your actual model — change this line!
model = tf.keras.models.load_model(
    r"E:\Desktop Backup\Documents\CYBERBOTDJANGO2.0\CYBERBOTDJANGO2\fake_real_model.h5"
)

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save as model.tflite in the same folder
with open(
    r"E:\Desktop Backup\Documents\CYBERBOTDJANGO2.0\CYBERBOTDJANGO2\model.tflite",
    "wb"
) as f:
    f.write(tflite_model)

print("✅ Conversion Successful! Saved as model.tflite")

