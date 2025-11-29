import tensorflow as tf

train_ds = tf.keras.utils.image_dataset_from_directory(
    'dataset/train', image_size=(600,600), batch_size=32, label_mode='int', shuffle=True
)
test_ds = tf.keras.utils.image_dataset_from_directory(
    'dataset/test', image_size=(2712,2700), batch_size=32, label_mode='int', shuffle=False
)

# Normalize
normalization_layer = tf.keras.layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y)).prefetch(tf.data.AUTOTUNE)
test_ds = test_ds.map(lambda x, y: (normalization_layer(x), y)).prefetch(tf.data.AUTOTUNE)

# Model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')   # 2 outputs for Fake/Real
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train
model.fit(train_ds, validation_data=test_ds, epochs=10)

# Save
model.save('fake_real_model.h5')
print("Model trained and saved!")
