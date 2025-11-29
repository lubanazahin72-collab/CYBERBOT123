history = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=10
)
