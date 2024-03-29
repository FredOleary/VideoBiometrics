import matplotlib.pyplot as plt
import numpy as np


class HRCharts:
    """Charts showing results of motion analysis of video """

    def __init__(self, logger):
        self.logger = logger
        self.chart_dictionary = {}

    def add_chart(self, name, sub_charts_rows=3, sub_charts_columns=1):
        self.chart_dictionary.update({name: self.__create_chart(name, sub_charts_rows, sub_charts_columns)})

    def close_all(self):
        plt.close('all')

    @staticmethod
    def __create_chart(name, sub_charts_rows, sub_charts_columns):
        fig, ax = plt.subplots(sub_charts_rows, sub_charts_columns)
        fig.suptitle(name, fontsize=14)

        return {"fig": fig, "ax": ax}

    def update_chart(self, tracker):
        """Update amplitude vs time and FFT charts"""
        self.chart_dictionary[tracker.name]["ax"][0][0].clear()
        self.chart_dictionary[tracker.name]["ax"][0][0].title.set_text("Raw RGB Data")
        self.chart_dictionary[tracker.name]["ax"][0][1].clear()
        self.chart_dictionary[tracker.name]["ax"][0][1].title.set_text("FFT RGB HR-Amplitude")
        self.chart_dictionary[tracker.name]["ax"][1][0].clear()
        self.chart_dictionary[tracker.name]["ax"][1][0].title.set_text("Filtered ICA RGB")
        self.chart_dictionary[tracker.name]["ax"][1][1].clear()
        self.chart_dictionary[tracker.name]["ax"][1][1].title.set_text("RGB PkPk HR-Amplitude")

        if tracker.time_period is not None and len(tracker.time_period) > 0:
            if tracker.type == "color":
                try:
                    bpm_pk = "N/A" if tracker.bpm_pk_pk is None else str(round(tracker.bpm_pk_pk, 2))
                    bpm_fft = "N/A" if tracker.bpm_fft is None else str(round(tracker.bpm_fft, 2))

                    self.chart_dictionary[tracker.name]["fig"].suptitle("{} BPM(pk-pk) {}. BPM(fft) {}".format(
                        tracker.name, bpm_pk, bpm_fft), fontsize=14)

                    if tracker.raw_amplitude_red is not None:
                        self.chart_dictionary[tracker.name]["ax"][0][0].plot(
                            tracker.time_period,
                            tracker.raw_amplitude_red,
                            label='Red Raw data',
                            color=(1.0, 0.0, 0.0))

                    if tracker.raw_amplitude_green is not None:
                        self.chart_dictionary[tracker.name]["ax"][0][0].plot(
                            tracker.time_period,
                            tracker.raw_amplitude_green,
                            label='Green Raw data',
                            color=(0.0, 1.0, 0.0))

                    if tracker.raw_amplitude_blue is not None:
                        self.chart_dictionary[tracker.name]["ax"][0][0].plot(
                            tracker.time_period,
                            tracker.raw_amplitude_blue,
                            label='Blue Raw data',
                            color=(0.0, 0.0, 1.0))

                    # self.chart_dictionary[tracker.name]["ax"][0][0].legend(loc='best')

                    if tracker.filtered_amplitude_red is not None:
                        self.chart_dictionary[tracker.name]["ax"][1][0].plot(
                            tracker.time_period,
                            tracker.filtered_amplitude_red,
                            label='Red ICA Filtered data',
                            color=(1.0, 0.0, 0.0))

                    if tracker.filtered_amplitude_green is not None:
                        self.chart_dictionary[tracker.name]["ax"][1][0].plot(
                            tracker.time_period,
                            tracker.filtered_amplitude_green,
                            label='Green ICA Filtered data',
                            color=(0.0, 1.0, 0.0))

                    if tracker.filtered_amplitude_blue is not None:
                        self.chart_dictionary[tracker.name]["ax"][1][0].plot(
                            tracker.time_period,
                            tracker.filtered_amplitude_blue,
                            label='Blue ICA Filtered data',
                            color=(0.0, 0.0, 1.0))

                    if tracker.peaks_positive_amplitude is not None:
                        self.chart_dictionary[tracker.name]["ax"][1][0].plot(
                            tracker.time_period[tracker.peaks_positive_amplitude],
                            tracker.pk_pk_series[tracker.peaks_positive_amplitude],
                            'ro', ms=3, label='Positive peaks',
                            color=(0.0, 0.0, 0.0))

                    # self.chart_dictionary[tracker.name]["ax"][1][0].legend(loc='best')

                    if tracker.fft_frequency is not None:
                        # chart_bar_width = (tracker.fft_frequency[len(tracker.fft_frequency) - 1] / (
                        #             len(tracker.fft_frequency) * 5))
                        chart_bar_width = (np.min(np.diff(tracker.fft_frequency)) / 5) * 60

                        self.chart_dictionary[tracker.name]["ax"][0][1].bar(tracker.fft_frequency *60,
                                                                            tracker.fft_amplitude_total,
                                                                            color=(0.0, 0.0, 0.0),
                                                                            width=chart_bar_width,
                                                                            label='Total Harmonics')
                        if tracker.fft_amplitude_red is not None:
                            self.chart_dictionary[tracker.name]["ax"][0][1].bar(
                                tracker.fft_frequency *60 + chart_bar_width,
                                tracker.fft_amplitude_red,
                                color=(1.0, 0.0, 0.0),
                                width=chart_bar_width,
                                label='Red harmonics')
                        if tracker.fft_amplitude_green is not None:
                            self.chart_dictionary[tracker.name]["ax"][0][1].bar(
                                tracker.fft_frequency *60 + 2 * chart_bar_width,
                                tracker.fft_amplitude_green,
                                color=(0.0, 1.0, 0.0),
                                width=chart_bar_width,
                                label='Green harmonics')
                        if tracker.fft_amplitude_blue is not None:
                            self.chart_dictionary[tracker.name]["ax"][0][1].bar(
                                tracker.fft_frequency * 60 + 3 * chart_bar_width,
                                tracker.fft_amplitude_blue,
                                color=(0.0, 0.0, 1.0),
                                width=chart_bar_width,
                                label='Blue harmonics')

                        # self.chart_dictionary[tracker.name]["ax"][0][1].legend(loc='best')
                    self.chart_dictionary[tracker.name]["ax"][0][1].set_xlim([40, 160])

                    if tracker.peaks_positive_red is not None:
                        self.chart_dictionary[tracker.name]["ax"][1][1].plot(
                            1 / (np.diff(tracker.peaks_positive_red) * tracker.time_period[1] - tracker.time_period[
                                0]) * 60,
                            tracker.filtered_amplitude_red[tracker.peaks_positive_red][1:],
                            'ro', ms=3, label='Positive peaks -Red',
                            color=(1.0, 0.0, 0.0))
                    if tracker.peaks_positive_green is not None:
                        self.chart_dictionary[tracker.name]["ax"][1][1].plot(
                            1 / (np.diff(tracker.peaks_positive_green) * tracker.time_period[1] - tracker.time_period[
                                0]) * 60,
                            tracker.filtered_amplitude_green[tracker.peaks_positive_green][1:],
                            'ro', ms=3, label='Positive peaks -Green',
                            color=(0.0, 1.0, 0.0))
                    if tracker.peaks_positive_blue is not None:
                        self.chart_dictionary[tracker.name]["ax"][1][1].plot(
                            1 / (np.diff(tracker.peaks_positive_blue) * tracker.time_period[1] - tracker.time_period[
                                0]) * 60,
                            tracker.filtered_amplitude_blue[tracker.peaks_positive_blue][1:],
                            'ro', ms=3, label='Positive peaks -Blue',
                            color=(0.0, 0.0, 1.0))
                    self.chart_dictionary[tracker.name]["ax"][1][1].set_xlim([40, 160])
                    self.chart_dictionary[tracker.name]["ax"][1][1].set_ylim([0, 1.05])

                except IndexError:
                    self.logger.error("charting error " + tracker.name)
        else:
            self.chart_dictionary[tracker.name]["fig"].suptitle(tracker.name + " BPM - Not available"
                                                                , fontsize=14)

        plt.ion()
        plt.pause(0.00001)
        plt.show()

    def update_fft_composite_chart(self, roi_composite, data):
        """Update FFT Composite charts"""
        self.chart_dictionary[data['name']]["ax"][0].clear()
        self.chart_dictionary[data['name']]["ax"][1].clear()
        try:
            bpm_fft = "N/A" if roi_composite.bpm_from_sum_of_ffts is None else \
                str(round(roi_composite.bpm_from_sum_of_ffts, 2))

            self.chart_dictionary[data['name']]["fig"].suptitle("{} BPM(fft) {}".format(
                data['name'], bpm_fft), fontsize=14)

            if ('fft_frequency1' in data and data['fft_frequency1'] is not None) and \
                    ('fft_frequency2' in data and data['fft_frequency2'] is not None):
                chart_bar_width = np.min(np.diff(data['fft_frequency1'])) / 3

                self.chart_dictionary[data['name']]["ax"][0].bar(
                    data['fft_frequency1'] - chart_bar_width, data['fft_amplitude1'],
                    color=(0.0, 0.0, 1.0), width=chart_bar_width,
                    label=data['fft_name1'])

                self.chart_dictionary[data['name']]["ax"][0].bar(
                    data['fft_frequency2'], data['fft_amplitude2'],
                    color=(0.0, 1.0, 0.0), width=chart_bar_width,
                    label=data['fft_name2'])

                self.chart_dictionary[data['name']]["ax"][0].legend(loc='best')

            if roi_composite.sum_of_ffts_frequency is not None:
                chart_bar_width = np.min(np.diff(roi_composite.sum_of_ffts_frequency)) / 2

                self.chart_dictionary[data['name']]["ax"][1].bar(
                    roi_composite.sum_of_ffts_frequency,
                    roi_composite.sum_of_ffts_amplitude,
                    color=(1.0, 0.0, 0.0), width=chart_bar_width,
                    label='Arithmetic sum of harmonics')

                self.chart_dictionary[data['name']]["ax"][1].legend(loc='best')

        except IndexError:
            self.logger.error("charting error " + data['name'])

        plt.ion()
        plt.pause(0.00001)
        plt.show()

    def update_correlated_composite_chart(self, name, roi_composite):
        """Update FFT Composite charts"""
        self.chart_dictionary[name]["ax"][0].clear()
        self.chart_dictionary[name]["ax"][1].clear()
        try:
            bpm_pk_pk = "N/A" if roi_composite.bpm_from_correlated_peaks is None else \
                str(round(roi_composite.bpm_from_correlated_peaks, 2))
            bpm_fft = "N/A" if roi_composite.bpm_from_correlated_ffts is None else \
                str(round(roi_composite.bpm_from_correlated_ffts, 2))

            self.chart_dictionary[name]["fig"].suptitle("{} BPM(pk-pk) {}. BPM(fft) {}".format(
                name, bpm_pk_pk, bpm_fft), fontsize=14)

            if roi_composite.correlated_y1_amplitude is not None:
                self.chart_dictionary[name]["ax"][0].plot(roi_composite.correlated_time_period,
                                                          roi_composite.correlated_y1_amplitude,
                                                          color=(0.0, 1.0, 0.0),
                                                          label='Y1 (filtered')

            if roi_composite.correlated_y2_amplitude is not None:
                self.chart_dictionary[name]["ax"][0].plot(roi_composite.correlated_time_period,
                                                          roi_composite.correlated_y2_amplitude,
                                                          color=(0.0, 1.0, 1.0),
                                                          label='Y2 (filtered')

            if roi_composite.correlated_amplitude is not None:
                self.chart_dictionary[name]["ax"][0].plot(roi_composite.correlated_time_period,
                                                          roi_composite.correlated_amplitude,
                                                          color=(1.0, 0.0, 0.0),
                                                          label='Sum of correlated series')

            if roi_composite.correlated_peaks_positive is not None:
                self.chart_dictionary[name]["ax"][0].plot(
                    roi_composite.correlated_time_period[roi_composite.correlated_peaks_positive],
                    roi_composite.correlated_amplitude[roi_composite.correlated_peaks_positive],
                    'ro', ms=3, label='positive peaks',
                    color=(0.0, 0.0, 1.0))

                self.chart_dictionary[name]["ax"][0].legend(loc='best')

            if roi_composite.correlated_fft_frequency is not None:
                chart_bar_width = np.min(np.diff(roi_composite.correlated_fft_frequency)) / 2

                self.chart_dictionary[name]["ax"][1].bar(
                    roi_composite.correlated_fft_frequency,
                    roi_composite.correlated_fft_amplitude,
                    color=(1.0, 0.0, 0.0), width=chart_bar_width,
                    label='Sum of correlated signals - harmonics')

                self.chart_dictionary[name]["ax"][1].legend(loc='best')

        except IndexError:
            self.logger.error("charting error " + name)

        plt.ion()
        plt.pause(0.00001)
        plt.show()
