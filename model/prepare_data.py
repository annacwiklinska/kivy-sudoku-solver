import os

import cv2


def prepare():
    path = "model/data/"
    with open("model/data_2.csv", "a+") as f:
        for filename in os.listdir(path):
            name = filename.split(".")[0]
            img = cv2.imread(os.path.join(path, filename), cv2.IMREAD_GRAYSCALE)
            if img is not None:  # Check if image loaded successfully
                img = cv2.resize(img, (28, 28))
                img = img.reshape(1, -1).flatten()
                img = ",".join(map(str, img))
                f.write(f"{name[0]},{img}\n")


prepare()
