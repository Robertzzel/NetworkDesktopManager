import sys
import sounddevice as sd
from configurations import Configurations
import zmq, signal
import zmq.sugar


class SoundGenerator:
    def __init__(self, port):
        self._device_index = self._get_device_index()
        self._context = zmq.Context()
        self._socket: zmq.sugar.Socket = self._context.socket(zmq.PUSH)
        self._socket.connect(f"tcp://localhost:{port}")

    def start(self):
        while True:
            rec = sd.rec(Configurations.SOUND_RECORD_SECONDS * Configurations.SOUND_FRAMES,
                         samplerate=Configurations.SOUND_FRAMES,
                         channels=Configurations.SOUND_CHANNELS, blocking=True)

            self._socket.send_pyobj((1, rec))

    def _get_device_index(self):
        for index, dev in enumerate(sd.query_devices()):
            if 'pulse' in dev['name']:
                return index
        raise Exception("Pulse device not found")

    def clean(self):
        self._context.destroy(linger=0)
        sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda x, y: sg.clean())
    if len(sys.argv) == 2:
        sg = SoundGenerator(sys.argv[1])
        sg.start()
    else:
        print("No port given")

