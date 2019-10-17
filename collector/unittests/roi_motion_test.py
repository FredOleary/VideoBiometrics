import unittest
import matplotlib.pyplot as plt
import numpy as np
from roi_motion import ROIMotion
from hr_charts import HRCharts
import logging
from utilities import read_config

class TestROIMotion(unittest.TestCase):

    def test_roi_motion(self):
        logger = logging.getLogger("foo")
        config = read_config()

        hr_chart = HRCharts(logger)
        hr_chart.add_chart("MotionChart")

        fps = 30.0  # frames/second (sample rate)
        sample_interval = 1.0 / fps  # sampling interval
        length_of_signal_seconds = 10
        pulse_rate_seconds = 1.0

        x_time = np.arange(0, length_of_signal_seconds, sample_interval)

        trend = np.linspace(0, 3, len(x_time))
        y = trend + np.sin(pulse_rate_seconds * 2.0 * np.pi * x_time) + .3 * np.sin(
            pulse_rate_seconds * 3 * 2.0 * np.pi * x_time)

        roi_motion = ROIMotion( logger, config, 'Y', 'MotionChart')

        roi_motion.initialize(0, y[0], 0, 0, None)

        for x in range(int(fps * length_of_signal_seconds) - 1):
            roi_motion.update(0, y[x + 1], 0, 0, None)

        roi_motion.process(fps, 30, 150)

        roi_motion.calculate_bpm_from_peaks_positive()

        roi_motion.calculate_bpm_from_fft()

        self.assertEqual(round(roi_motion.bpm_fft), 60.0)

        if roi_motion.bpm_pk_pk < 58 or roi_motion.bpm_pk_pk > 62:
            self.assertTrue(True, "roi_motion.bpm_pk-pk - out of range")
        hr_chart.update_chart(roi_motion)
        plt.show()
        input("Done - Press Enter/Return to exit")



if __name__ == '__main__':
    unittest.main()
