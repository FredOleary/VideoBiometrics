import numpy as np
import matplotlib.pyplot as plt

from bandpass_filter import BandPassFilter
from fft_filter import FFTFilter
from utilities import normalize_amplitude
from sklearn.decomposition import FastICA, PCA

a = np.array([[5, 55, 155],])

b = np.concatenate( (a, np.array([[6, 66, 166]],)))
avg = b.mean(axis=0)
c = np.array([[avg[0], avg[1], avg[2]]])


foo = np.loadtxt("color.csv", delimiter=',')
foo_norm = foo / foo.max(axis=0)

band_pass_filter = BandPassFilter()
blue_series = normalize_amplitude(foo[:,0])
green_series = normalize_amplitude(foo[:,1])
red_series = normalize_amplitude(foo[:,2])

filter_blue = band_pass_filter.time_filter2(blue_series, 30, 42, 150)
filter_green = band_pass_filter.time_filter2(green_series, 30, 42, 150)
filter_red = band_pass_filter.time_filter2(red_series, 30, 42, 150)

fft_filter = FFTFilter()
fft_frequency_blue, fft_amplitude_blue = fft_filter.fft_filter2(filter_blue, 30, 42, 150)
fft_frequency_green, fft_amplitude_green = fft_filter.fft_filter2(filter_green, 30, 42, 150)
fft_frequency_red, fft_amplitude_red = fft_filter.fft_filter2(filter_red, 30, 42, 150)

fig, ax = plt.subplots(3, 1)
fig.suptitle("Time series", fontsize=14)

ax[0].plot( blue_series, label='raw blue', color=(0,0,1))
ax[0].plot( filter_blue, label='filtered blue', color=(0,1,1))


ax[1].plot( green_series, label='raw green', color=(0,1,0))
ax[1].plot( filter_green, label='filtered green', color=(1,1,0))

ax[2].plot( red_series, label='raw red', color=(1,0,0))
ax[2].plot( filter_red, label='filtered red', color=(1,0,1))

fig2, ax2 = plt.subplots(2, 1)
fig2.suptitle("Harmonics", fontsize=14)

chart_bar_width = np.min(np.diff(fft_frequency_blue)) / 7

ax2[0].bar( fft_frequency_blue - chart_bar_width,fft_amplitude_blue, color=(0.3, 0.3, 1.0), width=chart_bar_width, label="blue")
ax2[0].bar( fft_frequency_green ,fft_amplitude_green, color=(0.3, 1.0, 0.3), width=chart_bar_width, label="green")
ax2[0].bar( fft_frequency_red + chart_bar_width,fft_amplitude_red, color=(1.0, 0.3, 0.3), width=chart_bar_width, label="red")


sum_fft = fft_amplitude_blue + fft_amplitude_green + fft_amplitude_red
ax2[1].bar(fft_frequency_red,sum_fft, color=(1.0, 0.0, 0.0), width=2*chart_bar_width, label="red")

A = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])  # Mixing matrix
S = np.c_[blue_series, green_series, red_series]

#S /= S.std(axis=0)  # Standardize data

#X = np.dot(S, A.T)  # Generate observations
ica = FastICA(n_components=3)
S_ = ica.fit_transform(S)  # Reconstruct signals

blue_xform = normalize_amplitude(S_[:,0])
filter_blue_xform = band_pass_filter.time_filter2(blue_xform, 30, 42, 150)
fft_frequency_blue_xform, fft_amplitude_blue_xform = fft_filter.fft_filter2(blue_xform, 30, 42, 150)

green_xform = normalize_amplitude(S_[:,1])
filter_green_xform = band_pass_filter.time_filter2(green_xform, 30, 42, 150)
fft_frequency_green_xform, fft_amplitude_green_xform = fft_filter.fft_filter2(green_xform, 30, 42, 150)

red_xform = normalize_amplitude(S_[:,2])
filter_red_xform = band_pass_filter.time_filter2(red_xform, 30, 42, 150)
fft_frequency_red_xform, fft_amplitude_red_xform = fft_filter.fft_filter2(red_xform, 30, 42, 150)

ax[0].plot( blue_xform, label='ICA blue', color=(1,0,1))
ax[0].plot( filter_blue_xform, label='ICA blue-Filtered', color=(.5,.5,1))
ax[1].plot( blue_xform, label='ICA Green', color=(0,1,0))
ax[1].plot( filter_blue_xform, label='ICA Green-Filtered', color=(.5,1,.5))
ax[2].plot( red_xform, label='ICA Red', color=(1,0,0))
ax[2].plot( filter_red_xform, label='ICA Red-Filtered', color=(1,.5,.5))


ax2[0].bar( fft_frequency_blue_xform + 2*chart_bar_width,fft_amplitude_blue_xform,  color=(0,0,.7), width=chart_bar_width, label="Blue_ICA")
ax2[0].bar( fft_frequency_green_xform + 3*chart_bar_width,fft_amplitude_green_xform,  color=(0,.7,0), width=chart_bar_width, label="Green_ICA")
ax2[0].bar( fft_frequency_red_xform + 4*chart_bar_width,fft_amplitude_red_xform,  color=(.7,0,0), width=chart_bar_width, label="Red_ICA")

sum_fft_xform = fft_amplitude_blue_xform + fft_amplitude_green_xform + fft_amplitude_red_xform

ax2[1].bar(fft_frequency_red_xform + 2*chart_bar_width, sum_fft_xform, color=(0.0, 1.0, 0.0), width=2*chart_bar_width, label="Xform - total")

ax[0].legend(loc = 'best')
ax2[1].legend(loc = 'best')

ax2[0].legend(loc = 'best')

plt.ion()
plt.pause(0.00001)
plt.show()
input("press enter")
print("fpp")
