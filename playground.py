import cv2
import numpy as np
import scipy.io.wavfile
from PIL.ImageGrab import grab
import time
import sounddevice as sd
import soundfile as sf
import pickle
from Commons.image_operations import *
from Tools.screenshot_tool import *
import struct


if __name__ == "__main__":
    x = "0012"
    enc = struct.pack(f'{len(x)}s', x.encode())
    dec = struct.unpack(f'{len(x)}s', enc)
    print(dec)

