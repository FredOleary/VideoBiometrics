import numpy as np
import matplotlib.pyplot as plt

from bandpass_filter import BandPassFilter
from fft_filter import FFTFilter
from utilities import normalize_amplitude
from sklearn.decomposition import FastICA, PCA

def calc_bpm():
    foo = np.loadtxt("color.csv", delimiter=',')

    fig, ax = plt.subplots(3, 1)
    fig.suptitle("Time series", fontsize=14)

    blue_series = normalize_amplitude(foo[:,0])
    green_series = normalize_amplitude(foo[:,1])
    red_series = normalize_amplitude(foo[:,2])

    ax[0].plot( blue_series, label='Normalized Raw Blue data', color=(0,0,1))
    ax[0].plot( red_series, label='Normalized Raw Red data', color=(1,0,0))
    ax[0].plot( green_series, label='Normalized Raw Green data', color=(0,1,0))

    band_pass_filter = BandPassFilter()

    filter_blue = blue_series.copy()
    filter_green = green_series.copy()
    filter_red = red_series.copy()

    # filter_blue = band_pass_filter.time_filter2(blue_series, 30, 42, 150)
    # filter_green = band_pass_filter.time_filter2(green_series, 30, 42, 150)
    # filter_red = band_pass_filter.time_filter2(red_series, 30, 42, 150)

    S = np.c_[filter_blue, filter_green, filter_red]
    ica = FastICA(n_components=3, max_iter=1000)
    S_ = ica.fit_transform(S)

    blue_xform = S_[:,0]
    green_xform = S_[:,1]
    red_xform = S_[:,2]

    # blue_xform = band_pass_filter.time_filter2(blue_xform, 30, 42, 150)
    # green_xform = band_pass_filter.time_filter2(green_xform, 30, 42, 150)
    # red_xform = band_pass_filter.time_filter2(red_xform, 30, 42, 150)


    ax[1].plot( blue_xform, label='ICA Blue data', color=(0,0,1))
    ax[1].plot( red_xform, label='ICA Red data', color=(1,0,0))
    ax[1].plot( green_xform, label='ICAGreen data', color=(0,1,0))

    fft_filter = FFTFilter()
    fft_frequency_blue_xform, fft_amplitude_blue_xform = fft_filter.fft_filter2(blue_xform, 30, 42, 150)
    fft_frequency_green_xform, fft_amplitude_green_xform = fft_filter.fft_filter2(green_xform, 30, 42, 150)
    fft_frequency_red_xform, fft_amplitude_red_xform = fft_filter.fft_filter2(red_xform, 30, 42, 150)

    fft_total_amplitude = fft_amplitude_blue_xform + fft_amplitude_green_xform +fft_amplitude_red_xform

    chart_bar_width = np.min(np.diff(fft_frequency_blue_xform)) / 5
    ax[2].bar( fft_frequency_blue_xform ,fft_amplitude_blue_xform,  color=(0,0,1), width=chart_bar_width, label="Blue_ICA")
    ax[2].bar( fft_frequency_green_xform + chart_bar_width,fft_amplitude_green_xform,  color=(0, 1, 0), width=chart_bar_width, label="Green_ICA")
    ax[2].bar( fft_frequency_red_xform + 2*chart_bar_width,fft_amplitude_red_xform,  color=(1,0,0), width=chart_bar_width, label="Red_ICA")
    ax[2].bar( fft_frequency_red_xform + 3*chart_bar_width,fft_total_amplitude,  color=(0,0,0), width=chart_bar_width, label="Total_ICA")

    freq_array = np.where(fft_total_amplitude == np.amax(fft_total_amplitude))
    if len(freq_array) > 0:
        # Use this index to get the corresponding frequency in beats/minute
        bpm = (fft_frequency_red_xform[freq_array[0]] * 60)[0]
        print("BPM {}".format((bpm)))



    ax[0].legend(loc = 'best')
    ax[1].legend(loc = 'best')
    ax[2].legend(loc = 'best')

    plt.ion()
    plt.pause(0.00001)
    plt.show()
    input("press enter")

if __name__ == '__main__':
    while True:
        calc_bpm()
