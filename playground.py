from queue import Queue
import sounddevice as sd
from threading import Thread
import numpy as np
import cv2

sd.default.device[0] = 2
print(sd.query_devices())
q = Queue()

def record():
    while True:
        print("recording")
        recording = sd.rec(3 * 44100, samplerate=44100, channels=2)
        sd.wait()
        print("done recording")
        q.put(recording)


def play():
    while True:
        recording = q.get()
        print("Playing")
        sd.play(recording)
        sd.wait()
        print("finish playing")

if __name__ == "__main__":
    Thread(target=play).start()
    record()






