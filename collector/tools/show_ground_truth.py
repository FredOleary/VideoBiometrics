import sys
import matplotlib.pyplot as plt
from ground_truth import GroundTruth


def process_ground_truth( file_name):
    ground_truth = GroundTruth(None, file_name)
    ground_truth.process_ground_truth(10)

    fig, ax = plt.subplots(2, 1)
    fig.suptitle("Time series", fontsize=14)

    ax[0].plot( ground_truth.time_base, ground_truth.ecg_wave, label='ECG Waveform', color=(0,0,1))
    ax[1].plot( ground_truth.time_base, ground_truth.ecg_heart_rate, label='ECG Heart rate', color=(1,0,0))
    ax[1].plot( ground_truth.time_base, ground_truth.ecg_average, label='ECG Heart rate (average)', color=(0,1,0))

    ax[0].legend(loc='best')
    ax[1].legend(loc='best')

    plt.ion()
    plt.pause(0.00001)
    plt.show()
    input("press enter")

def string_to_numeric_array( string):
    string_array = string.split()
    return list(map(float, string_array))

if __name__ == '__main__':
    file_name = "/Volumes/My Passport for Mac/sample_videos/subject1/ground_truth.txt"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    process_ground_truth(file_name)
