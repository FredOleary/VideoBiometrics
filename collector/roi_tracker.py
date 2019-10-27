import numpy as np
import abc


class ROITracker(abc.ABC):
    """ROITracker provides an abstract base class for trackers """
    def __init__(self, logger, config, name, type):
        self.logger = logger
        self.config = config
        self.name = name
        self.type = type
        self.time_period = None

    @abc.abstractmethod
    def initialize(self, x, y, w, h, frame):
        pass

    @abc.abstractmethod
    def update(self, x, y, w, h, frame):
        pass

    @abc.abstractmethod
    def process(self, fps, low_pulse_bpm, high_pulse_bpm):
        pass

    @abc.abstractmethod
    def calculate_bpm_from_peaks_positive(self):
        pass

    @abc.abstractmethod
    def calculate_bpm_from_fft(self):
        pass

    def create_time_period(self, fps):
        sample_interval = 1.0 / fps
        video_length = len(self.raw_amplitude) * sample_interval
        self.time_period = np.arange(0, video_length, sample_interval)


