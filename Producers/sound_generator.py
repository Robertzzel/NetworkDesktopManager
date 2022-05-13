import sounddevice as sd
from configurations import Configurations
import zmq
import sys


class SoundGenerator:
    def __init__(self, port):
        self._device_index = self._get_device_index()
        self._socket = zmq.Context().socket(zmq.REP)
        self._socket.connect(f"tcp://localhost:{port}")

    def start(self):
        try:
            while True:
                action = self._socket.recv()
                if action == b"0":
                    rec = sd.rec(Configurations.SOUND_RECORD_SECONDS * Configurations.SOUND_FRAMES,
                                 samplerate=Configurations.SOUND_FRAMES,
                                 channels=Configurations.SOUND_CHANNELS, blocking=True)
                    self._socket.send_pyobj(rec)
                elif action == b"1":
                    break
            print("Generator inchis")
        except:
            print("Generator inchis")

    def _get_device_index(self):
        for index, dev in enumerate(sd.query_devices()):
            if 'pulse' in dev['name']:
                return index
        raise Exception("Pulse device not found")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        SoundGenerator(sys.argv[1]).start()
