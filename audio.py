import pyaudio
import numpy as np
from scipy import signal
import struct
import time


chunk = 2048  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
while True:
    data = stream.read(chunk)

    data = np.frombuffer(data, dtype='b')
    f, t, Sxx = signal.spectrogram(data, fs=chunk)
    dBS = 10 * np.log10(Sxx)

    print(f)
    time.sleep(1/15000)

    # TODO: translate to duty cycles, also do the fft correctly and this other stuff we were talking about
