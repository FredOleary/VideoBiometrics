import numpy as np
from scipy import signal
from utilities import correlate_and_sum
from fft_filter import FFTFilter

class ROIComposite():
    """ROIComposite calculates data by 'combining' data from other ROI trackers """
    def __init__(self, logger, tracker_list):
        self.logger = logger
        self.tracker_list = tracker_list
        self.sum_of_ffts_amplitude = None
        self.sum_of_ffts_frequency = None
        self.correlated_amplitude = None
        self.correlated_time_period = None
        self.correlated_peaks_positive = None
        self.correlated_y1_amplitude = None
        self.correlated_y2_amplitude = None
        self.correlated_fft_amplitude = None
        self.correlated_fft_frequency = None
        self.bpm_from_sum_of_ffts = None
        self.bpm_from_correlated_peaks = None
        self.bpm_from_correlated_ffts = None
        self.name = 'ROI-Composite'

    def sum_ffts(self):
        """Calculate the composite FFT by arithmetically summing ffts """
        for tracker in self.tracker_list:
            if tracker.fft_amplitude is not None:
                if self.sum_of_ffts_amplitude is None:
                    self.sum_of_ffts_amplitude = np.copy(tracker.fft_amplitude)
                    self.sum_of_ffts_frequency = tracker.fft_frequency
                else:
                    self.sum_of_ffts_amplitude = np.add(self.sum_of_ffts_amplitude, tracker.fft_amplitude)

    def correlate_and_add(self, fps, low_pulse_bpm, high_pulse_bpm):
        """For now, this assumes there are only two series..."""
        if len(self.tracker_list) == 2 and \
                self.tracker_list[0].filtered_amplitude is not None and \
                self.tracker_list[1].filtered_amplitude is not None and \
                len(self.tracker_list[0].filtered_amplitude) == \
                len(self.tracker_list[1].filtered_amplitude) :
            y1_normalized = self.tracker_list[0].filtered_amplitude
            y2_normalized = self.tracker_list[1].filtered_amplitude

            self.correlated_y1_amplitude, self.correlated_y2_amplitude, self.correlated_amplitude = \
                correlate_and_sum(y1_normalized, y2_normalized)

            sample_interval = 1.0 / fps
            video_length = len(self.correlated_amplitude) * sample_interval
            self.correlated_time_period = np.arange(0, video_length, sample_interval)

            fft_filter = FFTFilter()
            self.correlated_fft_frequency, self.correlated_fft_amplitude = \
                fft_filter.fft_filter2(self.correlated_amplitude, fps, low_pulse_bpm, high_pulse_bpm)

            # Calculate pk-pk
            # since the data is normalize 0-2, set peak at 1.2 (The data is the sum of two 0-1 correlated signals)
            peaks_positive, _ = signal.find_peaks(self.correlated_amplitude, height=1.2, threshold=None)
            if len(peaks_positive) > 1:
                self.correlated_peaks_positive = peaks_positive;

    def calculate_bpm_from_peaks_positive(self):
        if self.correlated_peaks_positive is not None:
            time_intervals = np.average(np.diff(self.correlated_peaks_positive))
            per_beat_in_seconds = time_intervals * self.correlated_time_period[1] - self.correlated_time_period[0]
            self.bpm_from_correlated_peaks = 1 / per_beat_in_seconds * 60

    def calculate_bpm_from_sum_of_ffts(self):
        # Get the index of the maximum harmonic in the fft
        freq_array = np.where(self.sum_of_ffts_amplitude == np.amax(self.sum_of_ffts_amplitude))
        if len(freq_array) > 0:
            # Use this index to get the corresponding frequency in beats/minute
            self.bpm_from_sum_of_ffts = (self.sum_of_ffts_frequency[freq_array[0]] * 60)[0]

    def calculate_bpm_from_correlated_ffts(self):
        # Get the index of the maximum harmonic in the fft
        if self.correlated_fft_amplitude is not None:
            freq_array = np.where(self.correlated_fft_amplitude == np.amax(self.correlated_fft_amplitude))
            if len(freq_array) > 0:
                # Use this index to get the corresponding frequency in beats/minute
                self.bpm_from_correlated_ffts = (self.correlated_fft_frequency[freq_array[0]] * 60)[0]
