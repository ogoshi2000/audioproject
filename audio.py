import pyaudio
import numpy as np
import time
import sys
sys.path.append("../rpi-audio-levels")
from rpi_audio_levels import AudioLevels


def dBFS(x):
    return 10 * np.log10(x)


BITS_PER_CHUNK = 10
CHUNK = 2**BITS_PER_CHUNK
SAMPLE_FORMAT = pyaudio.paInt16
CHANNELS = 1
FS = 48000
BANDS_COUNT = 10
OC_BANDS = np.array([31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000])
F = np.fft.rfftfreq(CHUNK, 1. / FS)
fidx = []
for cf in OC_BANDS:
    fidx.append(list(np.where((F >= cf / np.sqrt(2)) & (F <= cf * np.sqrt(2)))))

p = pyaudio.PyAudio()
stream = p.open(format=SAMPLE_FORMAT,
                channels=CHANNELS,
                rate=FS,
                frames_per_buffer=CHUNK,
                input=True)
audio_levels = AudioLevels(BITS_PER_CHUNK, BANDS_COUNT)

while True:
    data = stream.read(CHUNK)
    data = np.frombuffer(data, dtype=np.int16)
    bands, _, _ = audio_levels.compute(data.astype(np.float32), fidx)
    print(bands)
    time.sleep(1)

p.close(stream)
