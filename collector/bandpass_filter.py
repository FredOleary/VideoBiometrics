from scipy.signal import butter, lfilter
import scipy.io
import numpy as np
from scipy import signal


class BandPassFilter:
    #    def __init__(self):

    @staticmethod
    def butter_bandpass(low_cut, high_cut, fs, order=5):
        nyq = 0.5 * fs
        low = low_cut / nyq
        high = high_cut / nyq
        # noinspection PyTupleAssignmentBalance
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, data, low_cut, high_cut, fs, order=5):
        b, a = self.butter_bandpass(low_cut, high_cut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    # def time_filter(self, y_amplitude, fps, low_pulse_bpm=None, high_pulse_bpm=None):
    #     if low_pulse_bpm is None:
    #         low_pulse_bps = 0
    #     else:
    #         low_pulse_bps = low_pulse_bpm/60
    #
    #     if high_pulse_bpm is None:
    #         high_pulse_bps = 10000
    #     else:
    #         high_pulse_bps = high_pulse_bpm/60
    #
    #     sample_interval = 1.0 / fps  # sampling interval
    #     video_length = len(y_amplitude) * sample_interval
    #     x_time = np.arange(0, video_length, sample_interval)  # time vector
    #     x_time = x_time[range(len(y_amplitude))]
    #
    #     if len(x_time > 0):
    #         y_amplitude_detrended = signal.detrend(y_amplitude)
    #         y_amplitude_filtered = self.butter_bandpass_filter(y_amplitude_detrended, low_pulse_bps, high_pulse_bps, fps, order=4)
    #
    #         # find peaks
    #         peaks_positive, _ = scipy.signal.find_peaks(y_amplitude_filtered, height=.2, threshold=None)
    #         if len(peaks_positive) > 1:
    #             time_intervals = np.average(np.diff(peaks_positive))
    #             per_beat_in_seconds = time_intervals * x_time[1]-x_time[0]
    #             beats_per_minute = 1/per_beat_in_seconds * 60
    #             return beats_per_minute, x_time, y_amplitude, y_amplitude_detrended, y_amplitude_filtered, peaks_positive
    #         else:
    #             return 0, x_time, y_amplitude, y_amplitude_detrended, y_amplitude_filtered, x_time
    #     # return unfiltered results.
    #     return 0, x_time, y_amplitude, y_amplitude, y_amplitude, x_time


    def time_filter2(self, amplitude, fps, low_pulse_bpm=None, high_pulse_bpm=None):
        if low_pulse_bpm is None:
            low_pulse_bps = 0
        else:
            low_pulse_bps = low_pulse_bpm/60

        if high_pulse_bpm is None:
            high_pulse_bps = 100000
        else:
            high_pulse_bps = high_pulse_bpm/60

        filtered_amplitude = self.butter_bandpass_filter(amplitude, low_pulse_bps, high_pulse_bps, fps, order=6)
        return filtered_amplitude
