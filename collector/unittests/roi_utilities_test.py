import unittest
import numpy as np
from utilities import BRG_mean


class TestUtilities(unittest.TestCase):

    def test_BRG_average(self):
        # Test BRG array - Note - Open cv uses BGR color rather than RGB color
        # 5* 4 matrix with RGB data => 20 values
        #manual calcs...
        # Avg of (19 *10 + 190)/20 = 19
        # Avg of (19 *20 + 380)/20 = 38
        # Avg of (19 *30 + 570)/20 = 57

        test_image = np.array([
                      [[10, 20, 30], [10, 20, 30], [10, 20, 30], [10, 20, 30], [10, 20, 30]],
                      [[10, 20, 30], [10, 20, 30], [10, 20, 30], [10, 20, 30], [10, 20, 30]],
                      [[10, 20, 30], [10, 20, 30], [10, 20, 30], [10, 20, 30], [10, 20, 30]],
                      [[10, 20, 30], [10, 20, 30], [10, 20, 30], [10, 20, 30], [190, 380, 570]]])

        average = BRG_mean(test_image)
        self.assertEqual(round(average[0]), 19)
        self.assertEqual(round(average[1]), 38)
        self.assertEqual(round(average[2]), 57)




if __name__ == '__main__':
    unittest.main()
