
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
        self.ecg_average_summary = list()


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
            self.ecg_average_summary.append(average)
            while next_index < stop and next_index < len(self.time_base):
                self.ecg_average[next_index] = average
                next_index += 1

    def get_next_average(self, index, average_in_seconds):
        start = index * average_in_seconds
        end = (index + 1) * average_in_seconds
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

    def get_average_for_period_ending(self, frame_no, frames_in_sample, fps ):
        """ Get the average heart rate for the previous period ending in frame_no """
        end_time = frame_no/fps
        sum = 0;
        index = 0
        count = 0
        average = 0
        start_time = end_time - frames_in_sample/fps
        if start_time < 0 :
            start_time = 0;
        for time in self.time_base:
            if time >= start_time and time <= end_time :
                sum += self.ecg_heart_rate[index]
                count += 1
            index += 1
        if count > 0:
            average = sum/count
        if self.logger is not None:
            self.logger.info( "Ground_truth between time {} - {}. ({} frames preceding frame {}. is {})".format(
                round(start_time,2), round(end_time,2), frames_in_sample, frame_no, round(average,2)))
        return average



