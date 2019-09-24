import scipy.io
import numpy as np


class FFTFilter:

    @staticmethod
    def filter_harmonics(x_frequency, y_frequency, low_pulse_bpm, high_pulse_bpm):
        start_index = 0
        end_index = x_frequency.size - 1
        low_pulse_bps = None
        high_pulse_bps = None
        if low_pulse_bpm is not None:
            low_pulse_bps = low_pulse_bpm/60
        if high_pulse_bpm is not None:
            high_pulse_bps = high_pulse_bpm/60

        for index in range(x_frequency.size):
            if low_pulse_bps is not None and x_frequency[index] > low_pulse_bps and start_index == 0:
                start_index = index
            if high_pulse_bps is not None and x_frequency[index] > high_pulse_bps:
                end_index = index
                break
        return x_frequency[start_index:end_index], y_frequency[start_index:end_index]

    def fft_filter(self, series, fps, dimension, low_pulse_bpm=None, high_pulse_bpm=None):
        ts = 1.0 / fps  # sampling interval

        video_length = len(series) * ts
        x_time = np.arange(0, video_length, ts)  # time vector
        x_time = x_time[range(len(series))]

        y_time = np.array(series)

        # persist to file for post processing
        # scipy.io.savemat('Pulse_time series_' + dimension, {
        #     'x': x_time,
        #     'y': y_time
        # })

        number_of_samples = len(y_time)  # length of the signal
        if number_of_samples > 0:
            k = np.arange(number_of_samples)
            x_frequency = k / video_length  # two sides frequency range
            x_frequency = x_frequency[range(int(number_of_samples / 2))]  # one side frequency range

            y_frequency = np.fft.fft(y_time) / number_of_samples  # fft computing and normalization
            y_frequency = abs(y_frequency[range(int(number_of_samples / 2))])

            x_frequency, y_frequency = self.filter_harmonics(x_frequency, y_frequency, low_pulse_bpm, high_pulse_bpm)
            return x_time, y_time, x_frequency, y_frequency
        else:
            # return empty arrays
            return np.array(series), np.array(series), np.array(series), np.array(series)

    def fft_filter2(self, amplitude_series, fps, low_pulse_bpm, high_pulse_bpm):
        ts = 1.0 / fps
        video_length = len(amplitude_series) * ts
        number_of_samples = len(amplitude_series)  # length of the signal
        if number_of_samples > 0:
            k = np.arange(number_of_samples)
            x_fft = k / video_length  # two sides frequency range
            x_fft = x_fft[range(int(number_of_samples / 2))]  # one side frequency range

            y_fft = np.fft.fft(amplitude_series) / number_of_samples  # fft computing and normalization
            y_fft = abs(y_fft[range(int(number_of_samples / 2))])

            x_fft, y_fft = self.filter_harmonics(x_fft, y_fft, low_pulse_bpm, high_pulse_bpm)

            return x_fft, y_fft
        else:
            # return empty arrays
            return None, None
