import cv2
import numpy as np
import scipy.io.wavfile
from PIL.ImageGrab import grab
import time
import sounddevice as sd
import soundfile as sf

def testare_ss():
    s = time.time()
    image = np.array(grab())
    image = cv2.resize(image, (800, 600), cv2.INTER_AREA)
    e1 = time.time()

    encoded = cv2.imencode(".jpg", image)[1]
    e2 = time.time()

    decoded = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    e3 = time.time()
    print((e3 - e2 + e2 - e1 + e1 - s) * 1000)
    cv2.imshow("das", decoded)
    cv2.waitKey(0)


if __name__ == "__main__":
    for index, dev in enumerate(sd.query_devices()):
        if 'pulse' in dev['name']:
            sd.default.device = index

    fs = int(44100/16)
    ch = 2
    sd.default.samplerate = fs
    sd.default.channels = ch

    myrec = sd.rec(int(fs * 10))
    sd.wait()
    #scipy.io.wavfile.write('out.wav', fs, myrec)
    encoded = myrec.tobytes()
    print("s-a scris in fisier")

    decoded = np.frombuffer(encoded, dtype=np.float32)
    decoded.shape = (decoded.shape[0]//2, 2)
    #data, fs = sf.read("out.wav", dtype='float32')
    sd.play(decoded, fs)
    sd.wait()

