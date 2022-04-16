import time

import cv2

class D:
    def __init__(self):
        self.D = 2

def f():
    for _ in range(5):
        time.sleep(1)
        yield D()

if __name__ == "__main__":
    for i in f():
        print(i.D)