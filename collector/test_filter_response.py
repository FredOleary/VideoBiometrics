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

def test( start, end, low_freq_bpm, high_freq_bpm, fps ):
    low_freq_hz = start/60
    high_freq_hz = end/60
    freq_range = np.linspace(low_freq_hz, high_freq_hz, (high_freq_hz - low_freq_hz)/0.1)

    rmsValue = []
    for freq in freq_range:
        length = 10
        fps = 30

        time_series = make_time_series(fps, length)
        amplitude_series = np.sin(freq * 2 * np.pi * time_series)
        band_pass_filter = BandPassFilter()
        filter_series = band_pass_filter.time_filter2(amplitude_series, fps, low_freq_bpm, high_freq_bpm)
        rmsValue.append( np.sqrt(np.mean(filter_series**2)))

        print("Freq: ", freq, "RMS value: ", rmsValue[len(rmsValue)-1])

    print("foo")

    fig, ax = plt.subplots(1, 1)
    fig.suptitle("Filter series", fontsize=14)

    ax.plot( freq_range, rmsValue, label='filter response')


    ax.legend(loc = 'best')

if __name__ == '__main__':
    test(10, 200, 40, 150, 30 ) # range 10->200bpm, filter 40bpm -> 150bpm, 30fps
    plt.ion()
    plt.pause(0.00001)
    plt.show()
    input("press enter")
