import pyaudio
import numpy as np
import time
import matplotlib.pyplot as plt
import board
import busio
import adafruit_pca9685

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

hat.frequency=1500
led_channel = hat.channels
print(led_channel)

for c in led_channel:
    c.duty_cycle=0


def dBFS(x):
    return 10*np.log10(x)


chunk = 2048 # Record in chunks of 1024 samples
fft_chunk = 2048
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 48000  # Record at 44100 samples per second
oc_bands = np.array([ 125, 250, 500, 1000, 2000, 4000, 8000, 16000])
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
# fig = plt.figure(1)
# ax1 = fig.add_subplot(211)
# ax2 = fig.add_subplot(212)
# fig.show()
# mx1 = 20000
# mx2 = 80

val = [100,100,100,100,100,100,100,100]
for c in led_channel:
    c.duty_cycle=0

while True:
                
    data = stream.read(chunk,exception_on_overflow=False)
    data = np.frombuffer(data, dtype=np.int16)
    fourier_data = np.fft.rfft(data)

    for i, idx in enumerate(fidx):
        bands[i] = dBFS(np.sqrt(np.sum(abs(fourier_data[idx])**2, axis=-1)))
    
    val_old = val[:]
    for i,v in enumerate(val):
        v = min(max(100,(bands[i]-55) * (2**(16)-1)/16),2**16-1)
        if v==100:
            v = val_old[i]

    for i,c in led_channel:
        c.duty_cycle = int(  (val[i]-100)**2/(2**16 -1)  )
    print(int(val[5]))

    # ax1.clear()
    # ax1.plot(data)
    # ax1.set_ylim([-mx1, mx1])
    # ax1.grid(b=True)

    # ax2.clear()
    # ax2.bar(np.arange(bands.shape[0]),
    #         bands,
    #         tick_label=[str(cf) for cf in oc_bands])

    # ax2.set_ylim([40, mx2])
    # ax2.grid(b=True)
    # fig.canvas.draw()

    # plt.pause(0.0001)
    time.sleep(1/1000)
    # TODO: translate to duty cycles

p.close(stream)
