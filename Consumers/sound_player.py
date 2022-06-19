import signal, sys, pathlib, zmq, zmq.sugar
sys.path.append(str(pathlib.Path(__file__).absolute().parent.parent))
import sounddevice as sd
from configurations import Configurations
from numpy import frombuffer, float32


class SoundPlayer:
    def __init__(self, port):
        self._context = zmq.Context()
        self._socket: zmq.sugar.Socket = self._context.socket(zmq.PULL)
        self._socket.connect(f"tcp://localhost:{port}")

    def start(self):
        while True:
            sounds = frombuffer(self._socket.recv_pyobj(), float32)
            sounds.shape = (sounds.shape[0]//Configurations.SOUND_CHANNELS, Configurations.SOUND_CHANNELS)
            sd.play(sounds, Configurations.SOUND_FRAMES)
            sd.wait()

    def clean(self):
        sd.stop()
        sd._terminate()
        self._context.destroy(linger=0)
        sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda x, y: sp.clean())
    if len(sys.argv) == 2:
        sp = SoundPlayer(sys.argv[1])
        sp.start()
    else:
        print("No port given")


