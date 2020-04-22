import pyaudio
import numpy as np
import time
import matplotlib.pyplot as plt

chunk = 2048  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
oc_bands = np.array([31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000])
f = np.fft.rfftfreq(chunk, 1. / fs)
fidx = []
for cf in oc_bands:
    fidx.append(np.where((f >= cf / np.sqrt(2)) & (f <= cf * np.sqrt(2))))
bands = np.zeros(oc_bands.shape)

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

# Store data in chunks for 3 seconds
fig = plt.figure(1)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
fig.show()
mx1 = 0
mx2 = 0

while True:
    data = stream.read(chunk)
    data = np.frombuffer(data, dtype=np.int16)
    fourier_data = np.fft.rfft(data)

    for i, idx in enumerate(fidx):
        bands[i] = np.sqrt(np.mean(abs(fourier_data[idx])**2, axis=-1))

    ax1.clear()
    ax1.plot(data)
    if np.max(np.abs(data)) > mx1:
        mx1 = np.max(np.abs(data))
        ax1.set_ylim([-mx1, mx1])
    ax1.grid(b=True)

    ax2.clear()
    ax2.bar(np.arange(bands.shape),
            bands,
            tick_label=[str(cf) for cf in oc_bands])
    if np.max(bands) > mx2:
        mx2 = np.max(bands)
        ax2.set_ylim([0, mx2])
    ax2.grid(b=True)
    fig.canvas.draw()

    time.sleep(0.01)
    plt.pause(0.001)
    # TODO: translate to duty cycles

p.close(stream)
