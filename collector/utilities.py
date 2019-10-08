import numpy as np
from numpy.fft import fft, ifft, fft2, fftshift
import uuid
CONFIG_FILE = "../config.txt"


def normalize_amplitude( data ):
    normalized_data = (data - np.min(data)) / np.ptp(data)
    return normalized_data

def BRG_mean( BRG_array):
    return np.mean(BRG_array,  axis=(0, 1))

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


def get_machine_id():
    return str(uuid.getnode())
    # TODO - implement for raspberry pi

def read_config():
    """Read the config.txt file. This is formatted as a python dictionary"""
    with open(CONFIG_FILE, 'r') as config:
        dict_from_file = eval(config.read())
    return dict_from_file
