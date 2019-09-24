import unittest
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from utilities import correlate_and_sum


class TestCorrelation(unittest.TestCase):

    def test_correlation(self):
        time_offset = .2

        fps = 30.0  # frames/second (sample rate)
        sample_interval = 1.0 / fps  # sampling interval
        length_of_signal_seconds = 10
        pulse_rate_seconds = 1.0

        x_time1 = np.arange(0, length_of_signal_seconds, sample_interval)
        y1 = np.sin(pulse_rate_seconds * 2.0 * np.pi * x_time1) * 6 # 6 unit sine wave

        x_time2 =  np.arange(time_offset, (length_of_signal_seconds + time_offset), sample_interval)  # offset by 10 units
        y2 = np.sin(pulse_rate_seconds * 2.0 * np.pi * x_time2) * 6 # 6 unit sine wave

        y_uncorrelated = y1+y2
        self.assertGreater(((max(y1) + max(y1)) - max(y_uncorrelated)), 2, "Correlation failure")

        x_time2 -= time_offset
        fig, ax = plt.subplots(2)
        fig.suptitle("Correlation - test", fontsize=14)

        ax[0].plot(x_time1, y1, label='Series 1', color=(1.0, 0.0, 0.0))
        ax[0].plot(x_time2, y2, label='Series 2', color=(0.0, 1.0, 0.0))

        y1, y2, y_correlated = correlate_and_sum( y1, y2 )
        x_correlated = x_time1[:len(y_correlated)]

        ax[1].plot(x_correlated, y_correlated, label='foo', color=(0.0, 0.0, 1.0))

        # since both y1&y2 are same amplitude, when correlated, the result should be 2 * y1
        #self.assertLessEqual((max(y_correlated) - (max(y1) + max(y1))), 0.001, "Correlation failure")
        plt.ion()
        plt.pause(0.00001)
        plt.show()


        input("Done - Press Enter/Return to exit")



if __name__ == '__main__':
    unittest.main()
