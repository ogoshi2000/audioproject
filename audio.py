import pyaudio
import numpy as np
import time


def dBFS(x):
    return 10 * np.log10(x)


CHUNK = 128
SAMPLE_FORMAT = pyaudio.paInt16
CHANNELS = 1
FS = 48000
OC_BANDS = np.array([31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000])
F = np.fft.rfftfreq(CHUNK, 1. / FS)
fidx = []
for cf in OC_BANDS:
    fidx.append(np.where((F >= cf / np.sqrt(2)) & (F <= cf * np.sqrt(2))))
bands = np.zeros(OC_BANDS.shape)

p = pyaudio.PyAudio()

stream = p.open(format=SAMPLE_FORMAT,
                channels=CHANNELS,
                rate=FS,
                frames_per_buffer=CHUNK,
                input=True)

while True:
    data = stream.read(CHUNK, exception_on_overflow=True)
    data = np.frombuffer(data, dtype=np.int16)
    fourier_data = np.fft.rfft(data)

    for i, idx in enumerate(fidx):
        bands[i] = dBFS(np.sqrt(np.sum(abs(fourier_data[idx])**2, axis=-1)))
    time.sleep(1)
    print(bands)

p.close(stream)
