import numpy as np
import time
from sklearn.decomposition import FastICA
from scipy import signal
from roi_tracker import ROITracker
from utilities import BRG_mean, normalize_amplitude
from fft_filter import FFTFilter
from bandpass_filter import BandPassFilter
import functools


class ROIColorICA(ROITracker):
    """ROIColorICA maintains raw and processed data for a RGB color changes """

    def __init__(self, logger, config, name, tracker_type):
        super().__init__(logger, config, name, tracker_type)
        # self.rgb_color = rgb_color
        # self.BRG_mean = None
        self.raw_amplitude = list()  # Raw data collected from video frames. (BGR format)
        self.raw_amplitude_red = None
        self.raw_amplitude_green = None
        self.raw_amplitude_blue = None

        self.filtered_amplitude_red = None
        self.filtered_amplitude_green = None
        self.filtered_amplitude_blue = None

        self.peaks_positive_red = None
        self.peaks_positive_green = None
        self.peaks_positive_blue = None

        self.fft_amplitude_red = None
        self.fft_amplitude_green = None
        self.fft_amplitude_blue = None

        self.fft_frequency = None
        self.fft_amplitude_total = None

        self.peaks_positive_amplitude = None
        self.pk_pk_series_label = None
        self.pk_pk_series = None

        self.bpm_pk_pk = None
        self.bpm_fft_confidence = None
        self.bpm_fft = None

    def initialize(self, x, y, w, h, frame):
        pass

    def update(self, x, y, w, h, frame):
        if x >= 0 and y >= 0:
            color_average, roi_filtered = self.__get_average(x, y, w, h, frame)
            self.raw_amplitude.append(color_average)
        else:
            if self.raw_amplitude is not None and len(self.raw_amplitude) > 0:
                self.raw_amplitude.append(self.raw_amplitude[len(self.raw_amplitude) - 1])

    def process(self, fps, low_pulse_bpm, high_pulse_bpm):
        start_time = time.time()

        if len(self.raw_amplitude) > 0:
            bgr_series = np.asarray(self.raw_amplitude)
            self.raw_amplitude_blue = normalize_amplitude(bgr_series[:, 0])
            self.raw_amplitude_green = normalize_amplitude(bgr_series[:, 1])
            self.raw_amplitude_red = normalize_amplitude(bgr_series[:, 2])
            self.logger.info("RBG Normalized at time {}".format(time.time() - start_time))

            self.__write_RGB_data_as_swift()
            band_pass_filter = BandPassFilter()
            blue_series = normalize_amplitude(
                band_pass_filter.time_filter2(self.raw_amplitude_blue, fps, low_pulse_bpm, high_pulse_bpm))
            green_series = normalize_amplitude(
                band_pass_filter.time_filter2(self.raw_amplitude_green, fps, low_pulse_bpm, high_pulse_bpm))
            red_series = normalize_amplitude(
                band_pass_filter.time_filter2(self.raw_amplitude_red, fps, low_pulse_bpm, high_pulse_bpm))

            if self.config["use_ICA"] is True:
                ica_series = np.c_[red_series, green_series, blue_series]
                ica = FastICA(random_state=1, tol=.0001, max_iter = 2000)
                ica_series = ica.fit_transform(ica_series)

                self.logger.info("ICA complete at time {}".format(time.time() - start_time))

                red_xform = normalize_amplitude(ica_series[:, 0])
                green_xform = normalize_amplitude(ica_series[:, 1])
                blue_xform = normalize_amplitude(ica_series[:, 2])
            else:
                red_xform = red_series
                green_xform = green_series
                blue_xform = blue_series

            self.filtered_amplitude_red = red_xform
            self.filtered_amplitude_green = green_xform
            self.filtered_amplitude_blue = blue_xform

            self.logger.info("ICA filtered at time {}".format(time.time() - start_time))

            fft_filter = FFTFilter()
            fft_frequency_red, self.fft_amplitude_red = fft_filter.fft_filter2(
                red_xform, fps, low_pulse_bpm, high_pulse_bpm)
            fft_frequency_green, self.fft_amplitude_green = fft_filter.fft_filter2(
                green_xform, fps, low_pulse_bpm, high_pulse_bpm)
            fft_frequency_blue, self.fft_amplitude_blue = fft_filter.fft_filter2(
                blue_xform, fps, low_pulse_bpm, high_pulse_bpm)

            self.fft_amplitude_total = self.fft_amplitude_blue + self.fft_amplitude_green + self.fft_amplitude_red
            self.fft_frequency = fft_frequency_green
            self.create_time_period(fps)

            # Pick the RGB component with the most dominant FFT frequency for pk-pk calculations
            max_value_r, max_index, confidence_r = self.__sort_fft(self.fft_amplitude_red)
            fft_red = ({"name": 'R', "series": self.filtered_amplitude_red, "confidence": max_value_r})

            max_value_g, max_index, confidence_g = self.__sort_fft(self.fft_amplitude_green)
            fft_green = ({"name": 'G', "series": self.filtered_amplitude_green, "confidence": max_value_g})

            max_value_b, max_index, confidence_b = self.__sort_fft(self.fft_amplitude_blue)
            fft_blue = ({"name": 'B', "series": self.filtered_amplitude_blue, "confidence": max_value_b})

            confidence_list = sorted((fft_red, fft_green, fft_blue), reverse=True,
                                     key=functools.cmp_to_key(self.__compare_confidence))

            self.pk_pk_series_label = confidence_list[0]["name"]
            self.pk_pk_series = confidence_list[0]["series"]

            peaks_positive, details = signal.find_peaks(self.pk_pk_series)
            tmp = np.diff(peaks_positive)

            self.peaks_positive_red, _ = signal.find_peaks(self.filtered_amplitude_red)
            self.peaks_positive_green, _ = signal.find_peaks(self.filtered_amplitude_green)
            self.peaks_positive_blue, _ = signal.find_peaks(self.filtered_amplitude_blue)

            self.logger.info("Pk-Pk Variance: Red: {}, : Green: {}, : Blue: {}".format(
                round(np.var(np.diff(self.peaks_positive_red))),
                round(np.var(np.diff(self.peaks_positive_green))),
                round(np.var(np.diff(self.peaks_positive_blue))))
            )

            if len(peaks_positive) > 2:
                self.peaks_positive_amplitude = peaks_positive

            self.logger.info("FFT completed at time {}".format(time.time() - start_time))

        self.logger.info("Process completed at time {}".format(time.time() - start_time))

    def __compare_confidence(self, item1, item2):
        if item1["confidence"] < item2["confidence"]:
            return -1
        else:
            return 1

    def calculate_bpm_from_peaks_positive(self, low_pulse_bpm, high_pulse_bpm):
        if self.peaks_positive_amplitude is not None:
            low_peak_count = (1/(low_pulse_bpm/60))/(self.time_period[1] - self.time_period[0])
            high_peak_count = (1/(high_pulse_bpm/60))/(self.time_period[1] - self.time_period[0])
            peak_counts =  np.diff(self.peaks_positive_amplitude)
            filtered_peak_counts = []
            for peak_count in peak_counts:
                if high_peak_count < peak_count < low_peak_count:
                    filtered_peak_counts.append(peak_count)
            if len(filtered_peak_counts) > 0:
                time_intervals = np.average(filtered_peak_counts)
                per_beat_in_seconds = time_intervals * (self.time_period[1] - self.time_period[0])
                self.bpm_pk_pk = 1 / per_beat_in_seconds * 60

    def calculate_bpm_from_fft(self):
        if self.fft_amplitude_total is not None:
            max_value, max_index, confidence = self.__sort_fft(self.fft_amplitude_total)
            self.bpm_fft = (self.fft_frequency[max_index] * 60)
            self.bpm_fft_confidence = confidence

    def __get_average(self, x, y, w, h, source_image):
        # If (x1,y1) and (x2,y2) are the two opposite vertices of mat
        # roi_filtered = source_image[y1:y2, x1:x2]
        # NOTE OpenCV uses BGR, NOT RGB
        roi_filtered = source_image[y:y + h, x:x + w]
        color_average = BRG_mean(roi_filtered)
        if self.config["headless"] is False:
            # set blue and red channels to 0
            roi_filtered[:, :, 0] = 0
            roi_filtered[:, :, 2] = 0

        return color_average, roi_filtered

    def __sort_fft(self, fft):
        """Process an FFT to return the value/index of the max frequency as well as confidence (0-100) that
        this frequency is dominant"""
        indices = fft.argsort()  # note: this is ascending
        max_index = indices[len(indices) - 1]
        max_value = fft[max_index]
        next_value = fft[indices[len(indices) - 2]]
        confidence = 100 - (next_value / max_value * 100)
        return max_value, max_index, confidence

    def __write_RGB_data_as_swift(self ):
        file_swift = open("sampleSwiftFormat.txt", "w")
        file_swift.write("let hrSampleBlue: [Double] {\n" )
        for i in range(256):
            file_swift.write( str(self.raw_amplitude_blue[i]) + ",\n")
        file_swift.write("\nlet hrSampleGreen: [Double] {\n" )
        for i in range(256):
            file_swift.write(str(self.raw_amplitude_green[i]) + ",\n")
        file_swift.write("\nlet hrSampleRed: [Double] {\n" )
        for i in range(256):
            file_swift.write(str(self.raw_amplitude_red[i]) + ",\n")

        file_swift.close()

