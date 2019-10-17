import unittest
import matplotlib.pyplot as plt
import numpy as np
import logging

from roi_color import ROIColor
from hr_charts import HRCharts
from utilities import read_config

class TestROIColor(unittest.TestCase):

    def test_roi_color(self):
        logger = logging.getLogger("foo")
        config = read_config()

        hr_chart = HRCharts(logger)
        hr_chart.add_chart("ColorChart")

        fps = 30.0  # frames/second (sample rate)
        sample_interval = 1.0 / fps  # sampling interval
        length_of_signal_seconds = 10
        pulse_rate_seconds = 1.0

        x_time = np.arange(0, length_of_signal_seconds, sample_interval)

        y = np.sin(pulse_rate_seconds * 2.0 * np.pi * x_time) * 6 # 6 pixel sine wave

        y = y+128 # biased around mid green (0-255 scale)

        rgb_array = np.zeros((512, 512, 3), 'uint8')
        rgb_array[..., 0] = .1 * 256
        rgb_array[..., 1] = .5 * 256
        rgb_array[..., 2] = .1 * 256

        roi_color = ROIColor( logger, config, 'G', 'ColorChart')

        roi_color.initialize(10,10, 100, 100, rgb_array)

        for x in range(int(fps * length_of_signal_seconds)):
            rgb_array[..., 1] = y[x]
            roi_color.update(10,10, 100, 100, rgb_array)

        roi_color.process(fps, 30, 150)

        roi_color.calculate_bpm_from_peaks_positive()

        roi_color.calculate_bpm_from_fft()

        if roi_color.bpm_pk_pk < 58 or roi_color.bpm_pk_pk > 62:
            self.assertTrue(True, "roi_color.bpm_peaks - out of range")
        self.assertEqual(round(roi_color.bpm_fft), 60.0)

        hr_chart.update_chart(roi_color)
        plt.show()
        input("Done - Press Enter/Return to exit")



if __name__ == '__main__':
    unittest.main()
