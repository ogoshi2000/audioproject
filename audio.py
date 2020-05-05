import pyaudio
import numpy as np
import time


def dBFS(x):
    return 10 * np.log10(x)


CHUNK = 512
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

packets = 0
lost = 0
while True:
    try:
        packets += 1
        data = stream.read(CHUNK, exception_on_overflow=True)
    except IOError:
        lost += 1
        print(str(lost) + '/' + str(lost))

    data = np.frombuffer(data, dtype=np.int16)
    fourier_data = np.fft.rfft(data)

    for i, idx in enumerate(fidx):
        bands[i] = dBFS(np.sqrt(np.sum(abs(fourier_data[idx])**2, axis=-1)))
    print(bands)

p.close(stream)
