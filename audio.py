import pyaudio
import numpy as np
import time
from multiprocessing import Queue
import scipy.fftpack


def dBFS(x):
    return 10 * np.log10(x)


###############################################################################
FFTCHUNK = 256
CHUNK = 128  #
OVERLAPS = 4  #
SAMPLE_FORMAT = pyaudio.paInt16  #
CHANNELS = 1  #
FS = 48000  #
OC_BANDS = np.array([31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000,
                     16000])  #
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

curr_chunk = np.zeros(CHUNK * OVERLAPS)
OL_IDX = [i * CHUNK / OVERLAPS for i in range(OVERLAPS * CHUNK / FFTCHUNK + 1)]
start = time.time()
try:
    while True:
        frame = frames.get()
        for i, j in zip(OL_IDX, OL_IDX[1:]):
            curr_chunk = np.concatenate(
                [curr_chunk[FFTCHUNK / OVERLAPS:], frame[i:j]])
            for k, idx in enumerate(fidx):
                fourier_data = scipy.fftpack.fft(curr_chunk)
                bands[k] = dBFS(
                    np.sqrt(np.sum(abs(fourier_data[idx])**2, axis=-1)))
            if int(time.time() - start) == 30:
                start = time.time()
                print(frames.qsize() * float(CHUNK) / FS)
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
