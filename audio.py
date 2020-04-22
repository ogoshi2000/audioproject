import pyaudio
import numpy as np
from scipy import signal
import struct


chunk = 1024  # Record in chunks of 1024 samples
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
    data = np.array(struct.unpack(str(2 * chunk) + 'B', data), dtype='b')
    f, t, Sxx = signal.spectrogram(data, fs=chunk)
    dBS = 10 * np.log10(Sxx)

    # TODO: translate to duty cycles, also do the fft correctly and this other stuff we were talking about
