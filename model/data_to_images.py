import time

import cv2
import numpy as np


def images():
    with open("data_2.csv", "r") as f:
        for line in f:
            line = line.strip().split(",")
            name = line[0]
            img = line[1:]
            img = np.array(img, dtype=np.uint8).reshape(28, 28)
            cv2.imwrite(f"images/{name}_{time.time()}.png", img)


images()
