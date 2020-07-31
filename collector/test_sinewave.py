import numpy as np
import matplotlib.pyplot as plt

from bandpass_filter import BandPassFilter
from fft_filter import FFTFilter
from utilities import normalize_amplitude

# def make_time_series():
#     return
red_only = True

def peak_detect( time_series, threshold):
    peaks = list()
    current_peak = -1
    for i in range(len(time_series)):
        if current_peak == -1:
            current_peak = i
        else:
            if time_series[i] > time_series[i-1]:
                current_peak = i
            elif time_series[i] <  time_series[i-1]:
                if (time_series[i-1] - time_series[i]) > threshold:
                    peaks.append(current_peak)
                    current_peak = -1





    return peaks

def make_time_series(sample_rate, length):
    time_series = np.linspace(0, length, sample_rate * length)
    return time_series

def test( hr ):

    length = 10
    # length = 8.53333
    fps = 30

    time_series = make_time_series(fps, length)


    # sampleRate = 30
    # frequency = 1.2
    # length = 10
    #
    # t = np.linspace(0, length, sampleRate * length)  # Produces a 5 second Audio-File
    # y = np.sin(frequency * 2 * np.pi * t)  # Has frequency of 440Hz

    red_series = np.sin(hr * 2 * np.pi * time_series)
    green_series = np.sin(1.0 * 2 * np.pi * time_series)
    blue_series = np.sin(1.05 * 2 * np.pi * time_series)

    foo = np.loadtxt("color.csv", delimiter=',')
    foo_norm = foo / foo.max(axis=0)


    band_pass_filter = BandPassFilter()
    # blue_series = normalize_amplitude(foo[:,0])
    # green_series = normalize_amplitude(foo[:,1])
    # red_series = normalize_amplitude(foo[:,2])

    filter_blue = band_pass_filter.time_filter2(blue_series, 30, 42, 150)
    filter_green = band_pass_filter.time_filter2(green_series, 30, 42, 150)
    filter_red = band_pass_filter.time_filter2(red_series, 30, 42, 150)

    fft_filter = FFTFilter()

    fft_frequency_blue, fft_amplitude_blue = fft_filter.fft_filter2(filter_blue, 30, 42, 150, filter = True)
    fft_frequency_green, fft_amplitude_green = fft_filter.fft_filter2(filter_green, 30, 42, 150, filter = True)
    fft_frequency_red, fft_amplitude_red = fft_filter.fft_filter2(filter_red, 30, 42, 150, filter = True)

    print("Freqs: ", fft_frequency_red * 60)

    red_index = fft_amplitude_red.argmax()
    green_index = fft_amplitude_green.argmax()
    blue_index= fft_amplitude_blue.argmax()

    fig, ax = plt.subplots(3, 1)
    fig.suptitle("Time series", fontsize=14)

    ax[2].plot( red_series, label='raw red {}'.format(hr *60), color=(1,0,0))
    ax[2].plot( filter_red, label='filtered red', color=(1,0,1))

    if red_only == False:
        ax[1].plot( green_series, label='raw green', color=(0,1,0))
        ax[1].plot( filter_green, label='filtered green', color=(1,1,0))

        ax[0].plot( blue_series, label='raw blue', color=(0,0,1))
        ax[0].plot( filter_blue, label='filtered blue', color=(0,1,1))

    fig2, ax2 = plt.subplots(1, 1)
    fig2.suptitle("Harmonics", fontsize=14)

    chart_bar_width = np.min(np.diff(fft_frequency_blue)) / 7

    ax2.bar( fft_frequency_red + chart_bar_width,fft_amplitude_red, color=(1.0, 0.3, 0.3), width=chart_bar_width,
             label="red {}/{}".format(round(fft_frequency_red[red_index] *60,2), round(hr*60,2)))
    if red_only == False:
        ax2.bar(fft_frequency_green, fft_amplitude_green, color=(0.3, 1.0, 0.3), width=chart_bar_width,
                label="green {}".format(fft_frequency_green[green_index]))
        ax2.bar( fft_frequency_blue - chart_bar_width,fft_amplitude_blue, color=(0.3, 0.3, 1.0), width=chart_bar_width, label="blue {}".format(fft_frequency_blue[blue_index]))




    ax[0].legend(loc = 'best')
    ax[1].legend(loc = 'best')
    ax[2].legend(loc = 'best')
    ax2.legend(loc = 'best')

if __name__ == '__main__':
    for hr in np.arange(60.0, 70.0, 0.1):
        test( hr/60 )
        plt.ion()
        plt.pause(0.00001)
        plt.show()
        input("press enter")
