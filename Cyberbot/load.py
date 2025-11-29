import tensorflow as tf

# Set paths 
train_dir = 'dataset/train'
test_dir = 'dataset/test'

# Load dataset
train_ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=(128, 128),  
    batch_size=32
)

test_ds = tf.keras.utils.image_dataset_from_directory(
   test_dir,
    image_size=(128, 128),
    batch_size=32
)



model = tf.keras.models.load_model("fake_real_model.h5")
print("Model loaded successfully!")

