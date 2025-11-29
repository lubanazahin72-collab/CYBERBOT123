import tensorflow as tf

# সঠিক path দিয়ে মডেল লোড করা
model = tf.keras.models.load_model(r"E:\Desktop Backup\Documents\CYBERBOTDJANGO2.0\CYBERBOTDJANGO2\fake_real_model.h5")


print("Model loaded successfully!")
