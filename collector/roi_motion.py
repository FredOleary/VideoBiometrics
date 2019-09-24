from roi_tracker import ROITracker


class ROIMotion(ROITracker):
    """ROIMotion maintains raw and processed data for a X/Y dimension of interest """
    def __init__(self, dimension, name):
        super().__init__(name)
        self.dimension = dimension

    def initialize(self, x, y, w, h, frame):
        value = x if self.dimension == 'X' else y
        super().initialize(value)

    def update(self, x, y, w, h, frame):
        value = x if self.dimension == 'X' else y
        self.add_value(value)

    def process(self, fps, low_pulse_bpm, high_pulse_bpm):
        self.create_time_period(fps)
#        self.de_trend_series()
        self.time_filter(fps, low_pulse_bpm, high_pulse_bpm)
        self.calculate_positive_peaks()
        self.fft_filter(fps, low_pulse_bpm, high_pulse_bpm)
        print( "processing")