from PIL import Image
import os

for subdir, dirs, files in os.walk("dataset"):
    for file in files:
        path = os.path.join(subdir, file)
        try:
            img = Image.open(path)
            img.verify()  # check if file is valid
        except Exception as e:
            print("Bad image:", path, e)
