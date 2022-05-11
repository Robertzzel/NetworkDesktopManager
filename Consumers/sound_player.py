import sounddevice as sd
from configurations import Configurations
from numpy import frombuffer, float32
import zmq, sys


class SoundPlayer:
    def __init__(self, port):
        self._socket = zmq.Context().socket(zmq.PAIR)
        self._socket.connect(f"tcp://localhost:{port}")
        print(f"Conecatat la {port}")

    def start(self):
        while True:
            action = self._socket.recv()
            if action == b"0":
                sound = self._socket.recv_pyobj()
                sounds = frombuffer(sound, float32)
                sounds.shape = (sounds.shape[0]//Configurations.SOUND_CHANNELS, Configurations.SOUND_CHANNELS)
                sd.play(sounds, Configurations.SOUND_FRAMES)
                sd.wait()
            elif action == b"1":
                sd.stop()
                sd._terminate()
                break
        print("Terminat")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        SoundPlayer(sys.argv[1]).start()
    else:
        print("No port given")


