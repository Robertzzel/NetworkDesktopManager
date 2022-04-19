import sounddevice as sd


if __name__ == "__main__":
    rec = sd.rec(3 * 44100, channels=2, blocking=True)
    sd.play(rec, blocking=True)
    sd.wait()