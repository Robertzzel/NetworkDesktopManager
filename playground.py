import cv2
import numpy as np
from PIL.ImageGrab import grab
import time

if __name__ == "__main__":
    s = time.time()
    image = np.array(grab())
    image = cv2.resize(image, (800, 600), cv2.INTER_AREA)
    e1 = time.time()

    encoded = cv2.imencode(".jpg", image)[1]
    e2 = time.time()

    decoded = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    e3 = time.time()
    print((e3-e2+e2-e1+e1-s)*1000)
    cv2.imshow("das", decoded)
    cv2.waitKey(0)
