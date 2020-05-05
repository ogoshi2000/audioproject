import pyaudio
import numpy as np
import time
from multiprocessing import Queue


def dBFS(x):
    return 10 * np.log10(x)


###############################################################################
CHUNK = 256*2  #
OVERLAPS = 2**2  #
SAMPLE_FORMAT = pyaudio.paInt16  #
CHANNELS = 1  #
FS = 48000  #
OC_BANDS = np.array([31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000,
                     16000])  #
###############################################################################

F = np.fft.rfftfreq(CHUNK, 1. / FS)
fidx = []
for cf in OC_BANDS:
    fidx.append(np.where((F >= cf / np.sqrt(2)) & (F <= cf * np.sqrt(2))))
bands = np.zeros(OC_BANDS.shape)

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

OLIDX = [i * CHUNK / OVERLAPS for i in range(OVERLAPS)]
print(OLIDX)
packets = 0
lost = 0

try:
    while True:
        print(frames.get())
        time.sleep(1)
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("ende wie der chris")
    quit()
# prev_chunk = stream.read(CHUNK, exception_on_overflow=True)
# prev_chunk = np.frombuffer(prev_chunk, dtype=np.int16)
# while True:
#     try:
#         packets += 1
#         curr_chunk = stream.read(CHUNK, exception_on_overflow=True)
#     except IOError:
#         lost += 1
#         print(str(lost) + '/' + str(packets))

#     curr_chunk = np.frombuffer(curr_chunk, dtype=np.int16)

#     for k in OLIDX:
#         fourier_data = np.fft.rfft(
#             np.concatenate([prev_chunk[:k], curr_chunk[k:]]))
#         for i, idx in enumerate(fidx):
#             bands[i] = dBFS(np.sqrt(np.sum(abs(fourier_data[idx])**2,
#                                            axis=-1)))

#     prev_chunk = curr_chunk
