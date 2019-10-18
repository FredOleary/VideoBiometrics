
import matplotlib.pyplot as plt

import os

class GroundTruth:
    def __init__(self, logger, file_name):
        self.logger = logger
        self.file_name = file_name
        self.ecg_wave = None;
        self.ecg_heart_rate = None;
        self.time_base = None;
        self.ecg_average = None;


    def process_ground_truth( self, average_in_sconds = None ):
        file = open(self.file_name, "r")
        self.ecg_wave  = file.readline()
        self.ecg_heart_rate = file.readline()
        self.time_base = file.readline()

        self.ecg_wave = self.string_to_numeric_array(self.ecg_wave)
        self.ecg_heart_rate = self.string_to_numeric_array(self.ecg_heart_rate)
        self.time_base = self.string_to_numeric_array(self.time_base)

        # Truncate to smallest array
        min_len = len(self.ecg_wave)
        if len(self.ecg_heart_rate) < min_len:
            min_len = len(self.ecg_heart_rate)
        if len(self.time_base) < min_len:
            min_len = len(self.time_base)
        del self.ecg_wave[min_len:]
        del self.ecg_heart_rate[min_len:]
        del self.time_base[min_len:]

        if average_in_sconds is not None:
            self. process_averages(average_in_sconds)


    def string_to_numeric_array( self, string):
        string_array = string.split()
        return list(map(float, string_array))

    def process_averages(self, average_in_sconds):
        #number of intervals to process
        self.ecg_average = [None] * len(self.time_base)
        intervals = int(self.time_base[len(self.time_base)-1]/average_in_sconds) +1
        next_index = 0
        for index in range(intervals):
            stop, average = self.get_next_average( index, average_in_sconds)
            while next_index < stop and next_index < len(self.time_base):
                self.ecg_average[next_index] = average
                next_index += 1

        print("foo")
    def get_next_average(self, index, average_in_indexsconds):
        start = index * average_in_indexsconds
        end = (index + 1) * average_in_indexsconds
        count = 0
        average = 0
        x = 0
        while self.time_base[x] < start:
            x += 1
        while x < len(self.ecg_heart_rate) and self.time_base[x] < end :
            average += self.ecg_heart_rate[x]
            count += 1
            x += 1
        average = average/count
        return x, average
