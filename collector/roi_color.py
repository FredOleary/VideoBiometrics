import numpy as np
from roi_tracker import ROITracker


class ROIColor(ROITracker):
    """ROIColor maintains raw and processed data for a RGB color changes """
    def __init__(self, logger, rgb_color, name):
        super().__init__(name)
        self.rgb_color = rgb_color
        self.logger = logger

    def initialize(self, x, y, w, h, frame):
        color_average, roi_filtered = self.__getAverage(x, y, w, h, frame)
        super().initialize(color_average)

    def update(self, x, y, w, h, frame ):
        if x >= 0 and y >= 0:
            color_average, roi_filtered = self.__getAverage(x, y, w, h, frame)
            self.add_value(color_average)
        else:
            self.add_value(0)

    def process(self, fps, low_pulse_bpm, high_pulse_bpm):
        self.create_time_period(fps)
#        self.de_trend_series()
        self.time_filter(fps, low_pulse_bpm, high_pulse_bpm)
        self.calculate_positive_peaks()
        self.fft_filter(fps, low_pulse_bpm, high_pulse_bpm)

    def __getAverage(self, x, y, w, h, source_image):
        # If (x1,y1) and (x2,y2) are the two opposite vertices of mat
        # roi_filtered = source_image[y1:y2, x1:x2]
        # NOTE OpenCV uses BGR, NOT RGB
        roi_filtered = source_image[y:y + h, x:x + w]

        if self.rgb_color == 'R':
            # set blue and green channels to 0
            roi_filtered[:, :, 0] = 0
            roi_filtered[:, :, 1] = 0
            avg_color_per_row = np.average(roi_filtered, axis=0)
            color_average = np.average(avg_color_per_row, axis=0)[2]
        elif self.rgb_color == 'B':
            # set green and red channels to 0
            roi_filtered[:, :, 1] = 0
            roi_filtered[:, :, 2] = 0
            avg_color_per_row = np.average(roi_filtered, axis=0)
            color_average = np.average(avg_color_per_row, axis=0)[0]
        else:
            # set blue and red channels to 0
            roi_filtered[:, :, 0] = 0
            roi_filtered[:, :, 2] = 0
            try:
                avg_color_per_row = np.average(roi_filtered, axis=0)
                color_average = np.average(avg_color_per_row, axis=0)[1]
            except ZeroDivisionError:
                if self.logger is not None:
                    self.logger.error("ZeroDivisionError - Exception!")
        return color_average, roi_filtered
