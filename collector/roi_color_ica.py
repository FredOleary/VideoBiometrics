import numpy as np
import time
from sklearn.decomposition import FastICA, PCA
from scipy import signal
from roi_tracker import ROITracker
from utilities import BRG_mean, normalize_amplitude
from fft_filter import FFTFilter
from bandpass_filter import BandPassFilter


class ROIColorICA(ROITracker):
    """ROIColorICA maintains raw and processed data for a RGB color changes """
    def __init__(self, logger, config, rgb_color, name):
        super().__init__(name)
        self.rgb_color = rgb_color
        self.logger = logger
        self.config = config
        self.BRG_mean = None

    def initialize(self, x, y, w, h, frame):
        self.BRG_mean, roi_filtered = self.__getAverage(x, y, w, h, frame)

    def update(self, x, y, w, h, frame ):
        if x >= 0 and y >= 0:
            color_average, roi_filtered = self.__getAverage(x, y, w, h, frame)
            self.raw_amplitude.append(color_average)
        else:
            if self.raw_amplitude is not None and len( self.raw_amplitude) > 0:
                self.raw_amplitude.append( self.raw_amplitude[len(self.raw_amplitude)-1])

    def process(self, fps, low_pulse_bpm, high_pulse_bpm):
        start_time = time.time()

        if len(self.raw_amplitude) > 0:
            BGR_series = np.asarray( self.raw_amplitude)
            blue_series = normalize_amplitude(BGR_series[:, 0])
            green_series = normalize_amplitude(BGR_series[:, 1])
            red_series = normalize_amplitude(BGR_series[:, 2])
            self.logger.info("RBG Normalized at time {}".format( time.time() -start_time))

            self.raw_amplitude = np.c_[blue_series, green_series, red_series]
            ica = FastICA(n_components=3)
            ICA_series = ica.fit_transform(self.raw_amplitude)

            self.logger.info("ICA complete at time {}".format( time.time() -start_time))

            blue_xform = ICA_series[:, 0]
            green_xform = ICA_series[:, 1]
            red_xform = ICA_series[:, 2]

            band_pass_filter = BandPassFilter()
            blue_xform = band_pass_filter.time_filter2(blue_xform, fps, low_pulse_bpm, high_pulse_bpm)
            green_xform = band_pass_filter.time_filter2(green_xform, fps, low_pulse_bpm, high_pulse_bpm)
            red_xform = band_pass_filter.time_filter2(red_xform, fps, low_pulse_bpm, high_pulse_bpm)

            self.filtered_amplitude = np.c_[blue_xform, green_xform, red_xform]
            height = .3 * np.max(green_xform)
            peaks_positive, _ = signal.find_peaks(green_xform, height = height, threshold=None)
            if len(peaks_positive) > 2:
                self.peaks_positive_amplitude = peaks_positive;
            else:
                self.peaks_positive_amplitude = None

            self.logger.info("ICA filtered at time {}".format(time.time() - start_time))

            fft_filter = FFTFilter()
            fft_frequency_blue_xform, fft_amplitude_blue_xform = fft_filter.fft_filter2(
                blue_xform, fps, low_pulse_bpm, high_pulse_bpm)
            fft_frequency_green_xform, fft_amplitude_green_xform = fft_filter.fft_filter2(
                green_xform, fps, low_pulse_bpm, high_pulse_bpm)
            fft_frequency_red_xform, fft_amplitude_red_xform = fft_filter.fft_filter2(
                red_xform, fps, low_pulse_bpm, high_pulse_bpm)

            self.fft_amplitude = fft_amplitude_blue_xform + fft_amplitude_green_xform + fft_amplitude_red_xform

            self.fft_frequency = fft_frequency_blue_xform

            self.create_time_period(fps)
            self.logger.info("FFT completed at time {}".format(time.time() - start_time))

        self.logger.info("Process completed at time {}".format(time.time() - start_time))


    def __getAverage(self, x, y, w, h, source_image):
        # If (x1,y1) and (x2,y2) are the two opposite vertices of mat
        # roi_filtered = source_image[y1:y2, x1:x2]
        # NOTE OpenCV uses BGR, NOT RGB
        roi_filtered = source_image[y:y + h, x:x + w]
        color_average = BRG_mean(roi_filtered)
        if self.config["headless"] is False:
            if self.rgb_color == 'R':
                # set blue and green channels to 0
                roi_filtered[:, :, 0] = 0
                roi_filtered[:, :, 1] = 0
            elif self.rgb_color == 'B':
                # set green and red channels to 0
                roi_filtered[:, :, 1] = 0
                roi_filtered[:, :, 2] = 0
            else:
                # set blue and red channels to 0
                roi_filtered[:, :, 0] = 0
                roi_filtered[:, :, 2] = 0

        return color_average, roi_filtered
