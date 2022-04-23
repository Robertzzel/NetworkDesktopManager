from queue import Queue
import sounddevice as sd
from threading import Thread
from multiprocessing import Process

sd.default.device[0] = 21
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
    Process(target=play).start()
    record()
    # sd.default.device[0] = 21
    # recording = sd.rec(2 * 44100, samplerate=44100, channels=2)
    # sd.wait()
    # sd.play(recording)
    # sd.wait()






