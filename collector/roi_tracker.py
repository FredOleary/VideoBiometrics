import numpy as np
from bandpass_filter import BandPassFilter
from fft_filter import FFTFilter
from scipy import signal
from utilities import normalize_amplitude

class ROITracker:
    """ROITracker maintains raw and processed data for the dimension of interest """
    def __init__(self, name):
        self.name = name
        self.time_period = None
        self.raw_amplitude = list()                 # Raw data collected from video frames
        self.de_trended_amplitude = None            # de-trended data
        self.filtered_amplitude = None              # time filtered
        self.peaks_positive_amplitude = None        # positive peaks.
        self.fft_amplitude = None                   # fft amplitude, from fft on time filtered data
        self.fft_frequency = None                   # fft harmonics
        self.bpm_pk_pk = None
        self.bpm_fft = None
        self.base_value = None
        self.bpm_fft_confidence = 100

    def initialize(self, initial_value):
        self.base_value = initial_value

    def add_value(self, value):
        self.raw_amplitude.append(value - self.base_value)

    def create_time_period(self, fps):
        sample_interval = 1.0 / fps
        video_length = len(self.raw_amplitude) * sample_interval
        self.time_period = np.arange(0, video_length, sample_interval)

    def de_trend_series(self):
        self.de_trended_amplitude = signal.detrend(self.raw_amplitude)

    def time_filter(self, fps, low_pulse_bpm, high_pulse_bpm):
        band_pass_filter = BandPassFilter()
        series = self.de_trended_amplitude if self.de_trended_amplitude is not None else self.raw_amplitude
        data = band_pass_filter.time_filter2(series, fps, low_pulse_bpm, high_pulse_bpm)
        self.filtered_amplitude = normalize_amplitude(data)

    def calculate_positive_peaks(self):
        #since the data is normalize 0-1, set peak at .6
        peaks_positive, _ = signal.find_peaks(self.filtered_amplitude, height=.6, threshold=None)
        if len(peaks_positive) > 1:
            # time_intervals = np.average(np.diff(peaks_positive))
            # per_beat_in_seconds = time_intervals * x_time[1] - x_time[0]
            # beats_per_minute = 1 / per_beat_in_seconds * 60
            self.peaks_positive_amplitude = peaks_positive;
        else:
            self.peaks_positive_amplitude = None

    def calculate_bpm_from_peaks_positive(self):
        if self.peaks_positive_amplitude is not None:
            time_intervals = np.average(np.diff(self.peaks_positive_amplitude))
            per_beat_in_seconds = time_intervals * self.time_period[1] - self.time_period[0]
            self.bpm_pk_pk = 1 / per_beat_in_seconds * 60

    def calculate_bpm_from_fft(self):
        if self.fft_amplitude is not None:
            freqArray = np.where(self.fft_amplitude == np.amax(self.fft_amplitude))
            if len(freqArray) > 0:
                self.bpm_fft = (self.fft_frequency[freqArray[0]] * 60)[0]
                # Calculate confidence, as a percentage, of the best BPM calculation
                self.bpm_fft_confidence = 100
                best = self.fft_amplitude[freqArray[0]]
                bestIndex = freqArray[0]
                self.fft_amplitude[freqArray[0]] = 0
                freqArray = np.where(self.fft_amplitude == np.amax(self.fft_amplitude))
                if len(freqArray) > 0:
                    next = self.fft_amplitude[freqArray[0]]
                    self.bpm_fft_confidence = 100 - (next[0]/best[0] * 100)

                self.fft_amplitude[bestIndex] = best

    def fft_filter(self, fps, low_pulse_bpm, high_pulse_bpm):
        """Note this requires that the raw data is previously filtered"""
        fft_filter = FFTFilter()
        self.fft_frequency, self.fft_amplitude = \
            fft_filter.fft_filter2(self.filtered_amplitude, fps, low_pulse_bpm, high_pulse_bpm)


