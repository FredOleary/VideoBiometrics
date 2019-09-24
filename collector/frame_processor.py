import time
import os
import numpy as np

import cv2

from frame_grabber import FrameGrabber
from raspberian_grabber import RaspberianGrabber

from roi_selector import ROISelector
from roi_motion import ROIMotion
from roi_color import ROIColor
from roi_composite import ROIComposite
from hr_charts import HRCharts
from reporters.csv_reporter import CSVReporter
from reporters.http_reporter import HTTPReporter


SUM_FTT_COMPOSITE = "Sum-of-FFTs"
CORRELATED_SUM = "Correlated-Sum"


# noinspection PyUnresolvedReferences
class FrameProcessor:
    def __init__(self, config):
        print("FrameProcessor:__init__ - openCV version: {}".format( cv2.__version__))
        print("FrameProcessor:__init__ - Configuration: ", config)
        self.config = config
        self.start_sample_time = None
        self.pulse_rate_bpm = "Not available"
        self.tracker = None
        self.frame_number = 0
        self.start_process_time = None
        self.tracker_list = list()
        self.hr_charts = None
        self.roi_selector = ROISelector(config)
        self.last_frame = None
        self.csv_reporter = CSVReporter()
        self.HTTPReporter = HTTPReporter(self.config)
        self.hr_estimate_count = 0

    def capture(self, video_file_or_camera: str):
        """Open video file or start camera. Then start processing frames for motion"""
        print("FrameProcessor:capture")

        csv_file = video_file_or_camera
        if video_file_or_camera is None:
            video_file_or_camera = 0  # First camera
            csv_file = "camera"

        video = self.__create_camera(video_file_or_camera, self.config["video_fps"],
                                   self.config["resolution"]["width"],
                                   self.config["resolution"]["height"])

        is_opened = video.open_video(video_file_or_camera)
        if not is_opened:
            print("FrameProcessor:capture - Error opening video stream or file, '{}'".format(video_file_or_camera))
        else:
            self.csv_reporter.open(csv_file)

            # retrieve the camera/video properties.
            width, height = video.get_resolution()
            self.config["resolution"]["width"] = width
            self.config["resolution"]["height"] = height
            self.config["video_fps"] = video.get_frame_rate()

            print("FrameProcessor:capture - Video: Resolution = {} X {}. Frame rate {}".
                  format(self.config["resolution"]["width"],
                         self.config["resolution"]["height"],
                         round(self.config["video_fps"])))

            self.__process_feature_detect_then_track(video)

        cv2.destroyWindow('Frame')
        self.csv_reporter.close()
        video.close_video()
        time.sleep(.5)
        input("Hit Enter to exit")

    def __start_capture(self, video):
        """Start streaming the video file or camera"""
        self.__create_trackers()
        self.frame_number = 0
        self.start_process_time = time.time()
        video.start_capture(self.config["pulse_sample_frames"]+1)

    def __process_feature_detect_then_track(self, video):
        """Read video frame by frame and collect changes to the ROI. After sufficient
        frames have been collected, analyse the results"""
        tracking = False

        self.__start_capture(video)
        if self.config["show_pulse_charts"] is True:
            self.hr_charts = HRCharts()
            for tracker in self.tracker_list:
                self.hr_charts.add_chart(tracker.name)

            self.hr_charts.add_chart(SUM_FTT_COMPOSITE, sub_charts = 2)
            self.hr_charts.add_chart(CORRELATED_SUM, sub_charts = 2)

        while video.is_opened():
            ret, frame = video.read_frame()
            if ret:
                # If the original frame is not writable and we wish to modify the frame. E.g. change the ROI to green
                self.last_frame = frame.copy()
                self.frame_number += 1
                if not tracking:
                    found, x, y, w, h = self.roi_selector.select_roi(self.last_frame)
                    if found:
                        print("FrameProcessor:process_feature_detect_then_track - Tracking after face detect")
                        for tracker in self.tracker_list:
                            tracker.initialize(x, y, w, h, self.last_frame)

                        cv2.rectangle(self.last_frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
                        track_box = (x, y, w, h)
                        self.tracker = cv2.TrackerCSRT_create()
                        self.tracker.init(self.last_frame, track_box)
                        tracking = True
                    else:
                        self.__start_capture(video)
                else:
                    # Update tracker
                    ok, bbox = self.tracker.update(self.last_frame)
                    if ok:
                        x = int(bbox[0])
                        y = int(bbox[1])
                        w = int(bbox[2])
                        h = int(bbox[3])
                        for tracker in self.tracker_list:
                            tracker.update(x, y, w, h, self.last_frame)
                        cv2.rectangle(self.last_frame, (x, y), (x + w, y + h), (225, 0, 0), 1)
                    else:
                        print("FrameProcessor:process_feature_detect_then_track - Tracker failed")
                        self.__start_capture(video)
                        tracking = False

                pulse_rate = self.pulse_rate_bpm if isinstance(self.pulse_rate_bpm, str) else round(self.pulse_rate_bpm, 2)
                cv2.putText(self.last_frame, "Pulse rate (BPM): {}. Frame: {}".format(pulse_rate, self.frame_number),
                            (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                cv2.imshow('Frame', self.last_frame)

                if self.frame_number > self.config["pulse_sample_frames"]:
                    self.__update_results(video.get_frame_rate())
                    print("FrameProcessor:process_feature_detect_then_track - Processing time: {} seconds. FPS: {}. Frame count: {}".
                          format(round(time.time() - self.start_process_time, 2),
                          round(self.frame_number / (time.time() - self.start_process_time), 2), self.frame_number))
                    if self.config["pause_between_samples"]:
                        input("Hit enter to continue")
                    self.__start_capture(video)
                    tracking = False
                # Press Q on keyboard to  exit
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            else:
                print("FrameProcessor:process_feature_detect_then_track - Video stream ended")
                break
        return

    def __update_results(self, fps):
        """Process the the inter-fame changes, and filter results in both time and frequency domain """
        self.hr_estimate_count += 1
        result_summary ={
            "passCount": self.hr_estimate_count,
            "trackers": {}
        }

        roi_composite = ROIComposite(self.tracker_list)

        composite_data_summ_fft = {
            "bpm_fft": None,
            "name": SUM_FTT_COMPOSITE,
        }

        index = 1;
        for tracker in self.tracker_list:
            tracker.process(fps, self.config["low_pulse_bpm"], self.config["high_pulse_bpm"])
            tracker.calculate_bpm_from_peaks_positive()
            tracker.calculate_bpm_from_fft()

            result_summary["trackers"].update({'{}PkPk'.format(tracker.name): round(tracker.bpm_pk_pk, 2)})
            result_summary["trackers"].update({'{}FFT'.format(tracker.name): round(tracker.bpm_fft, 2)})

            composite_data_summ_fft.update({'fft_frequency' + str(index) : tracker.fft_frequency} )
            composite_data_summ_fft.update({'fft_amplitude' + str(index): tracker.fft_amplitude})
            composite_data_summ_fft.update({'fft_name' + str(index): tracker.name})

            self.hr_charts.update_chart(tracker)
            index +=1

        roi_composite.sum_ffts()
        roi_composite.correlate_and_add(fps, self.config["low_pulse_bpm"], self.config["high_pulse_bpm"])
        roi_composite.calculate_bpm_from_sum_of_ffts()
        roi_composite.calculate_bpm_from_peaks_positive()
        roi_composite.calculate_bpm_from_correlated_ffts()

        result_summary.update({"sumFFTs": self.__round(roi_composite.bpm_from_sum_of_ffts)})
        result_summary.update({"correlatedPkPk": self.__round(roi_composite.bpm_from_correlated_peaks)})
        result_summary.update({"correlatedFFTs": self.__round(roi_composite.bpm_from_correlated_ffts)})

        if roi_composite.bpm_from_sum_of_ffts is not None:
            # TODO - Strategy to determine the 'best' heart rate
            self.pulse_rate_bpm = roi_composite.bpm_from_sum_of_ffts
        else:
            self.pulse_rate_bpm = "Not available"

        self.hr_charts.update_fft_composite_chart(roi_composite, composite_data_summ_fft)
        self.hr_charts.update_correlated_composite_chart(CORRELATED_SUM, roi_composite)

        self.csv_reporter.report_results( result_summary)
        self.http_reporter.report_results( result_summary)

    def __round(self, value, precision = 2):
        return None if value is None else round(value, precision)

    # def __result_summary_to_csv(self, results):
    #     if results["passCount"] == 1:
    #         # write the one time header
    #         csv_header = "Pass count,"
    #         for key in results["trackers"]:
    #             csv_header = csv_header + "{},".format(key)
    #         csv_header = csv_header + "Sum of FFTs, Correlated Pk-Pk, Correlated FFTs\n"
    #         self.hr_csv.write(csv_header)
    #
    #     csv_line = '{},'.format(results["passCount"])
    #     for value in results["trackers"].values():
    #         csv_line = csv_line + "{},".format(self.__round(value))
    #
    #     csv_line = csv_line + "{}, {}, {}\n".format(
    #         results["sumFFTs"], results["correlatedPkPk"], results["correlatedFFTs"])
    #     self.hr_csv.write(csv_line)

    # def __result_to_server(self, results):
    #     if results["passCount"] == 1:
    #         self.http_client.register()
    #
    #     self.http_client.send_heart_rate(results)

    def __create_trackers(self):
        self.tracker_list.clear()
        self.tracker_list.append(ROIMotion('Y', "vertical"))
        self.tracker_list.append(ROIColor('G', "green"))

    @staticmethod
    def __create_camera(video_file_or_camera, fps, width, height):
        """Create the appropriate class using opencv or the raspberry Pi piCamera"""
        # For files nor non raspberry pi devices, use opencv, for real-time video on raspberry pi, use CameraRaspbian
        if os.path.isfile("/etc/rpi-issue") and video_file_or_camera == 0:
            return RaspberianGrabber(cv2, fps, width, height)
        else:
            return FrameGrabber(cv2, fps, width, height)
