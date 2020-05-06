from __future__ import division
import pyaudio
import numpy as np
import time
from multiprocessing import Queue
import scipy.fftpack


def dBFS(x):
    return 10 * np.log10(x)


###############################################################################
FFTCHUNK = 1024
CHUNK = 128  #
SAMPLE_FORMAT = pyaudio.paInt16  #
CHANNELS = 1  #
FS = 48000  #
OC_BANDS = np.array([0, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000])  #
###############################################################################

F = np.fft.rfftfreq(FFTCHUNK, 1. / FS)
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

curr_chunk = np.zeros(FFTCHUNK)
start = time.time()
try:
    while True:
        curr_chunk = np.concatenate([curr_chunk[CHUNK:], frames.get()])
        for k, idx in enumerate(fidx):
            fourier_data = scipy.fftpack.fft(curr_chunk)
            bands[k] = dBFS(np.sqrt(np.sum(abs(fourier_data[idx])**2,
                                           axis=-1)))

        if int(time.time() - start) == 30:
            start = time.time()
            delay = frames.qsize() * CHUNK
            print("\ncurrent delay: %.1f ms" %
                  (frames.qsize() * CHUNK / FS * 1000))
            print(bands.round(decimals=2))
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("\n")
    print("queue size")
    q = frames.qsize()
    print(q)
    print("current delay")
    print(q * float(CHUNK) / FS)
    print("elapsed time:")
    print((time.time() - start))

    frames.close()
    print("ende wie der chris")
    quit()
