import numpy as np
import matplotlib.pyplot as plt
import statistics

from bandpass_filter import BandPassFilter
from utilities import normalize_amplitude
from sklearn.decomposition import FastICA

LOW_HEART_RATE_PER_MIN = 42
HIGHT_HEART_RATE_PER_MIN = 150

RED_PIXELS = "55-RedRaw.txt"
GREEN_PIXELS = "55-GreenRaw.txt"
BLUE_PIXELS = "55-BlueRaw.txt"

def process_samples( heart_rate_data ):

    heart_rate_data.TimeSeries = np.linspace(0, 10, 300)
    heart_rate_data.RawRedPixels = np.loadtxt(RED_PIXELS)
    heart_rate_data.RawGreenPixels = np.loadtxt(GREEN_PIXELS)
    heart_rate_data.RawBluePixels = np.loadtxt(BLUE_PIXELS)

    heart_rate_data.NormalizeRawRedPixels = normalize_amplitude(heart_rate_data.RawRedPixels)
    heart_rate_data.NormalizeRawGreenPixels = normalize_amplitude(heart_rate_data.RawGreenPixels)
    heart_rate_data.NormalizeRawBluePixels = normalize_amplitude(heart_rate_data.RawBluePixels)

    band_pass_filter = BandPassFilter()
    heart_rate_data.FilterRed = normalize_amplitude(band_pass_filter.time_filter2(heart_rate_data.NormalizeRawRedPixels, 30, 42, 150))
    heart_rate_data.FilterGreen = normalize_amplitude(band_pass_filter.time_filter2(heart_rate_data.NormalizeRawGreenPixels, 30, 42, 150))
    heart_rate_data.FilterBlue = normalize_amplitude(band_pass_filter.time_filter2(heart_rate_data.NormalizeRawBluePixels, 30, 42, 150))

    heart_rate_data.RedMax, heart_rate_data.RedMin = peakdetect(heart_rate_data.FilterRed, heart_rate_data.TimeSeries, 10, 0.01)
    heart_rate_data.GreenMax, heart_rate_data.GreenMin = peakdetect(heart_rate_data.FilterGreen, heart_rate_data.TimeSeries, 10, 0.01)
    heart_rate_data.BlueMax, heart_rate_data.BlueMin = peakdetect(heart_rate_data.FilterBlue, heart_rate_data.TimeSeries, 10, 0.01)

    print("foo")


def peakdetect(y_axis, x_axis=None, lookahead=500, delta=0):
    """
    Converted from/based on a MATLAB script at http://billauer.co.il/peakdet.html

    Algorithm for detecting local maximas and minmias in a signal.
    Discovers peaks by searching for values which are surrounded by lower
    or larger values for maximas and minimas respectively

    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- A x-axis whose values correspond to the 'y_axis' list and is used
        in the return to specify the postion of the peaks. If omitted the index
        of the y_axis is used. (default: None)
    lookahead -- (optional) distance to look ahead from a peak candidate to
        determine if it is the actual peak (default: 500)
        '(sample / period) / f' where '4 >= f >= 1.25' might be a good value
    delta -- (optional) this specifies a minimum difference between a peak and
        the following points, before a peak may be considered a peak. Useful
        to hinder the algorithm from picking up false peaks towards to end of
        the signal. To work well delta should be set to 'delta >= RMSnoise * 5'.
        (default: 0)
            Delta function causes a 20% decrease in speed, when omitted
            Correctly used it can double the speed of the algorithm

    return -- two lists [maxtab, mintab] containing the positive and negative
        peaks respectively. Each cell of the lists contains a tupple of:
        (position, peak_value)
        to get the average peak value do 'np.mean(maxtab, 0)[1]' on the results
    """
    maxtab = []
    mintab = []
    dump = []  # Used to pop the first hit which always if false

    length = len(y_axis)
    if x_axis is None:
        x_axis = range(length)

    # perform some checks
    if length != len(x_axis):
        raise (ValueError, "Input vectors y_axis and x_axis must have same length")
    if lookahead < 1:
        raise (ValueError, "Lookahead must be above '1' in value")
    if not (np.isscalar(delta) and delta >= 0):
        raise (ValueError, "delta must be a positive number")

    # needs to be a numpy array
    y_axis = np.asarray(y_axis)

    # maxima and minima candidates are temporarily stored in
    # mx and mn respectively
    mn, mx = np.Inf, -np.Inf

    # Only detect peak if there is 'lookahead' amount of points after it
    for index, (x, y) in enumerate(zip(x_axis[:-lookahead], y_axis[:-lookahead])):
        if y > mx:
            mx = y
            mxpos = x
        if y < mn:
            mn = y
            mnpos = x

        ####look for max####
        if y < mx - delta and mx != np.Inf:
            # Maxima peak candidate found
            # look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index + lookahead].max() < mx:
                maxtab.append((mxpos, mx))
                dump.append(True)
                # set algorithm to only find minima now
                mx = np.Inf
                mn = np.Inf

        ####look for min####
        if y > mn + delta and mn != -np.Inf:
            # Minima peak candidate found
            # look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index + lookahead].min() > mn:
                mintab.append((mnpos, mn))
                dump.append(False)
                # set algorithm to only find maxima now
                mn = -np.Inf
                mx = -np.Inf

    # Remove the false hit on the first value of the y_axis
    try:
        if dump[0]:
            maxtab.pop(0)
            # print "pop max"
        else:
            mintab.pop(0)
            # print "pop min"
        del dump
    except IndexError:
        # no peaks were found, should the function return empty lists?
        pass

    return maxtab, mintab


def analyse_heart_rate( name, time_series, peak):
    freqs = []
    if len( time_series ) > 1 :
        for i in range(len(time_series) -1 ):
            heart_rate_per_min = 1/(time_series[i+1] - time_series[i]) *60
            if heart_rate_per_min >= LOW_HEART_RATE_PER_MIN and heart_rate_per_min <= HIGHT_HEART_RATE_PER_MIN:
                freqs.append(heart_rate_per_min)

    if len( freqs ):
        print( "{}. Peak:{:.2f}. Average: {:.1f}. Number of samples: {}. Std deviation: {:.1f}".format( name, peak, np.average(freqs), len(freqs), statistics.stdev(freqs)))



class HeartRateData:
    TimeSeries = []

    RawRedPixels = []
    RawGreenPixels = []
    RawBluePixels = []

    NormalizeRawRedPixels = []
    NormalizeRawGreenPixels = []
    NormalizeRawBluePixels = []

    FilterRed = []
    FilterGreen = []
    FilterBlue = []

    GreenMax = []
    GreenMin = []

    RedMax = []
    RedMin = []



if __name__ == "__main__":
    heart_rate_data = HeartRateData()

    process_samples(heart_rate_data)

    fig2, ax = plt.subplots(2, 1)
    ax[0].plot(heart_rate_data.TimeSeries, heart_rate_data.RawRedPixels, label='Raw data', color=(1, 0, 0))
    ax[0].plot(heart_rate_data.TimeSeries, heart_rate_data.RawGreenPixels, label='Raw data', color=(0, 1, 0))
    ax[0].plot(heart_rate_data.TimeSeries, heart_rate_data.RawBluePixels, label='Raw data', color=(0, 0, 1))

    ax[1].plot(heart_rate_data.TimeSeries, heart_rate_data.FilterRed, label='Filtered data', color=(1, 0, 0))
    ax[1].plot(heart_rate_data.TimeSeries, heart_rate_data.FilterGreen, label='Filtered data', color=(0, 1, 0))
    ax[1].plot(heart_rate_data.TimeSeries, heart_rate_data.FilterBlue, label='Filtered data', color=(0, 0, 1))

    xm = [p[0] for p in heart_rate_data.RedMax]
    ym = [p[1] for p in heart_rate_data.RedMax]
    ax[1].plot(xm, ym, 'r+')

    xm = [p[0] for p in heart_rate_data.GreenMax]
    ym = [p[1] for p in heart_rate_data.GreenMax]
    ax[1].plot(xm, ym, 'g+')

    xm = [p[0] for p in heart_rate_data.BlueMax]
    ym = [p[1] for p in heart_rate_data.BlueMax]
    ax[1].plot(xm, ym, 'b+')


    # show range of heart rate adjusting peak threshold
    peak = 0.01
    while peak < 0.25:

        red_max, _ = peakdetect(heart_rate_data.FilterRed, heart_rate_data.TimeSeries, 10, peak)
        green_max, _ = peakdetect(heart_rate_data.FilterGreen, heart_rate_data.TimeSeries, 10, peak)
        blueMax, _ = peakdetect(heart_rate_data.FilterBlue, heart_rate_data.TimeSeries, 10, peak)
        xm = [p[0] for p in red_max]
        analyse_heart_rate( "Red", xm, peak )
        xm = [p[0] for p in green_max]
        analyse_heart_rate( "Green", xm, peak )
        xm = [p[0] for p in blueMax]
        analyse_heart_rate( "Blue", xm, peak )
        print("")
        peak += .01


    fig2.suptitle("RawWaveform", fontsize=14)
    plt.ion()
    plt.pause(0.00001)
    plt.show()
    input("press enter")
