import numpy as np
from numpy.fft import fft, ifft, fft2, fftshift


def normalize_amplitude( data ):
    normalized_data = (data - np.min(data)) / np.ptp(data)
    return normalized_data

def correlate_and_sum(y1, y2):
    """Correlate two signals and return the summed difference"""

    shift = __compute_shift(y1, y2)
    if shift > 0:
        #Y1 leads Y2, so shift Y2 back to Y1
        y2_shift = y2[shift:]
        y1_shift = y1[:len(y1)-shift]
        return y1_shift, y2_shift, y1_shift + y2_shift
    elif shift < 0:
        # Y2 leads Y1, so shift Y1 back to Y2
        shift = -shift
        y1_shift = y1[shift:]
        y2_shift = y2[:len(y2)-shift]
        return y1_shift, y2_shift, y1_shift + y2_shift
    else:
        return y1, y2, y1 + y2


def __compute_shift(y1, y2):
    """The shift factor return indicates how much y2 must be shifted for maximum correlation with y1 """
    assert len(y1) == len(y2)
    c = __cross_correlation_using_fft(y1, y2)
    assert len(c) == len(y1)
    zero_index = int(len(y1) / 2) - 1
    shift = zero_index - np.argmax(c)
    return shift


def __cross_correlation_using_fft(y1, y2):
    f1 = fft(y1)
    f2 = fft(np.flipud(y2))
    cc = np.real(ifft(f1 * f2))
    return fftshift(cc)
