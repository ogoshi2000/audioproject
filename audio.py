import pyaudio
import numpy as np
import time
from multiprocessing import Queue
import scipy as sp


def dBFS(x):
    return 10 * np.log10(x)


###############################################################################
CHUNK = 64  #
OVERLAPS = 4  #
SAMPLE_FORMAT = pyaudio.paInt16  #
CHANNELS = 1  #
FS = 48000  #
OC_BANDS = np.array([31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000,
                     16000])  #
###############################################################################

F = np.fft.rfftfreq(CHUNK * OVERLAPS, 1. / FS)
fidx = []
for cf in OC_BANDS:
    fidx.append(np.where((F >= cf / np.sqrt(2)) & (F <= cf * np.sqrt(2))))
bands = np.zeros(OC_BANDS.shape)
print(fidx)

p = pyaudio.PyAudio()

frames = Queue()


def callback(in_data, frame_count, time_info, status):
    global frames
    frames.put(np.frombuffer(in_data, dtype=np.int16))
    return (in_data, pyaudio.paContinue)


stream = p.open(format=SAMPLE_FORMAT,
                channels=CHANNELS,
                rate=FS,
                frames_per_buffer=CHUNK,
                input=True,
                stream_callback=callback)

curr_chunk = np.zeros(CHUNK * OVERLAPS)
OLIDX = [i * CHUNK / OVERLAPS for i in range(OVERLAPS)]

try:
    while True:
        curr_chunk = np.concatenate([curr_chunk[CHUNK:], frames.get()])
        fourier_data = sp.fft.rfft(curr_chunk)
        for i, idx in enumerate(fidx):
            bands[i] = dBFS(np.sqrt(np.sum(abs(fourier_data[idx])**2,
                                           axis=-1)))
    print(bands)
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("\n")
    print(frames.qsize())
    frames.close()
    print("ende wie der chris")
    quit()
