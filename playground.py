import threading
import time

from Producers.sound_generator import SoundGenerator
from Consumers.sound_player import SoundPlayer
from Producers.image_generator import ImageGenerator
from Consumers.image_displayer import ImageDisplayer
from multiprocessing import Queue

if __name__ == "__main__":
    q = Queue(1)
    ig = SoundGenerator(q)
    id = SoundPlayer(q)
    ig.start()
    id.start()

    time.sleep(1)
    ig.stop()
    id.stop()
    time.sleep(2)
    print(threading.active_count())