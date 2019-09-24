import numpy as np
from numpy.fft import fft, ifft, fft2, ifft2, fftshift
import matplotlib.pyplot as plt

def cross_correlation_using_fft(x, y):
    f1 = fft(x)
    f2 = fft(np.flipud(y))
    cc = np.real(ifft(f1 * f2))
    return fftshift(cc)

# shift &lt; 0 means that y starts 'shift' time steps before x # shift &gt; 0 means that y starts 'shift' time steps after x
def compute_shift(x, y):
    assert len(x) == len(y)
    c = cross_correlation_using_fft(x, y)
    assert len(c) == len(x)
    zero_index = int(len(x) / 2) - 1
    shift = zero_index - np.argmax(c)
    return shift


time_offset = .3

fps = 30.0  # frames/second (sample rate)
sample_interval = 1.0 / fps  # sampling interval
length_of_signal_seconds = 10
pulse_rate_seconds = 1.0

x_time1 = np.arange(0, length_of_signal_seconds, sample_interval)
y1 = np.sin(pulse_rate_seconds * 2.0 * np.pi * x_time1) * 6  # 6 unit sine wave

x_time2 = np.arange(time_offset, (length_of_signal_seconds + time_offset), sample_interval)  # offset by 10 units
y2 = np.sin(pulse_rate_seconds * 2.0 * np.pi * x_time2) * 6  # 3 unit sine wave

x_time2 -= time_offset

fig, ax = plt.subplots(2)
fig.suptitle("Correlation - test", fontsize=14)

ax[0].plot(x_time1, y1, label='Series 1', color=(1.0, 0.0, 0.0))
ax[0].plot(x_time2, y2, label='Series 2', color=(0.0, 1.0, 0.0))


foo = compute_shift(y1, y2)
print(foo)
y2_shift = y2[foo:]
y1_shift = y1[:len(y1)-foo]

# y2_shift = y2[:len(y1)-foo]
# y1_shift = y1[foo:]

x_time_shift = x_time1[:len(y1_shift)]

ax[1].plot(x_time_shift, y1_shift, label='Series 1', color=(1.0, 0.0, 0.0))
ax[1].plot(x_time_shift, y2_shift, label='Series 2', color=(0.0, 1.0, 0.0))

plt.ion()
plt.pause(0.00001)
plt.show()
