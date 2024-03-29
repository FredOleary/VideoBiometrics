import time
import os
import sys
import cv2

from frame_grabber import FrameGrabber
from raspberian_grabber import RaspberianGrabber

from roi_selector import ROISelector
from hr_charts import HRCharts
from reporters.csv_reporter import CSVReporter
from reporters.http_reporter import HTTPReporter
from roi_color_ica import ROIColorICA
from ground_truth import GroundTruth

SUM_FTT_COMPOSITE = "Sum-of-FFTs"
CORRELATED_SUM = "Correlated-Sum"
DEPRECATED = True

COLOR_PKPK = 'colorPkPk'
COLOR_FFT = 'colorFFT'
CONFIDENCE = 'FFTConfidence'


# noinspection PyUnresolvedReferences,SpellCheckingInspection
class FrameProcessor:
    def __init__(self, config, logger):
        self.logger = logger
        self.logger.info("openCV version: {}".format(cv2.__version__))
        self.logger.info("Configuration: {} ".format(config))
        self.config = config
        self.start_sample_time = None
        self.pulse_rate_bpm_pk_pk = "N/A"
        self.pulse_rate_bpm_fft = "N/A"
        self.tracker = None
        self.frame_number = 0
        self.total_frames_read = 0
        self.start_process_time = None
        self.tracker_list = list()
        self.hr_charts = None
        self.roi_selector = ROISelector(config)
        self.last_frame = None
        self.csv_reporter = CSVReporter()
        self.http_reporter = HTTPReporter(self.logger, self.config)
        self.hr_estimate_count = 0
        self.ground_truth = None

    def capture(self, video_file_or_camera: str):
        """Open video file or start camera. Then start processing frames for motion"""
        self.logger.info("Capture")

        csv_file = video_file_or_camera
        if video_file_or_camera is None:
            video_file_or_camera = 0  # First camera
            csv_file = "camera"

        video = self.__create_camera(video_file_or_camera,
                                     self.config["video_fps"],
                                     self.config["resolution"]["width"],
                                     self.config["resolution"]["height"])

        is_opened = video.open_video(video_file_or_camera)
        if not is_opened:
            self.logger.error("Error opening video stream or file, '{}'".format(video_file_or_camera))
        else:
            self.csv_reporter.open(csv_file)
            self.total_frames_read = 0

            # retrieve the camera/video properties.
            width, height = video.get_resolution()
            self.config["resolution"]["width"] = width
            self.config["resolution"]["height"] = height
            self.config["video_fps"] = video.get_frame_rate()
            self.logger.info("Capture - Video: Resolution = {} X {}. Frame rate {}".format(
                self.config["resolution"]["width"],
                self.config["resolution"]["height"],
                round(self.config["video_fps"])))

            if self.config["ground_truth"]:
                self.__process_ground_truth(video_file_or_camera)

            self.__process_feature_detect_then_track(video, video_file_or_camera)

            cv2.destroyAllWindows()
            self.csv_reporter.close()

        video.close_video()
        time.sleep(.5)
        if self.config["headless"] is False and self.config["pause_on_exit"] is True:
            input("Hit Enter to exit")
        if self.hr_charts is not None:
            self.hr_charts.close_all()

    def __start_capture(self, video):
        """Start streaming the video file or camera"""
        self.__create_trackers()
        self.frame_number = 0
        self.start_process_time = time.time()
        video.start_capture(self.config["pulse_sample_frames"] + 1)

    def __process_feature_detect_then_track(self, video, video_file_or_camera):
        """Read video frame by frame and collect changes to the ROI. After sufficient
        frames have been collected, analyse the results"""
        tracking = False

        self.__start_capture(video)
        if self.config["headless"] is False:
            self.hr_charts = HRCharts(self.logger)
            for tracker in self.tracker_list:
                self.hr_charts.add_chart(tracker.name, sub_charts_rows=2, sub_charts_columns=2)

        while video.is_opened():
            ret, frame = video.read_frame()
            if ret:
                self.total_frames_read += 1
                if self.config["headless"] is False:
                    # If the original frame is not writable and we wish to modify the frame. E.g.change the ROI to Pk-Pk
                    self.last_frame = frame.copy()
                else:
                    self.last_frame = frame

                self.frame_number += 1
                if not tracking:
                    found, x, y, w, h = self.roi_selector.select_roi(self.last_frame)
                    if found:
                        self.logger.info("Tracking after face detect")
                        for tracker in self.tracker_list:
                            tracker.initialize(x, y, w, h, self.last_frame)

                        cv2.rectangle(self.last_frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
                        track_box = (x, y, w, h)
                        self.logger.info("Using {} tracker".format(self.config["opencv_tracker"]))
                        if self.config["opencv_tracker"] == "CSRT":
                            self.tracker = cv2.TrackerCSRT_create()
                        elif self.config["opencv_tracker"] == "MOSSE":
                            self.tracker = cv2.TrackerMOSSE_create()
                        else:
                            self.tracker = cv2.TrackerKCF_create()

                        # self.tracker = cv2.TrackerCSRT_create()
                        # self.tracker = cv2.TrackerKCF_create()
                        # self.tracker = cv2.TrackerMOSSE_create()
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
                        if self.config["headless"] is False:
                            cv2.rectangle(self.last_frame, (x, y), (x + w, y + h), (225, 0, 0), 1)
                    else:
                        self.logger.warning("Tracker failed")
                        self.__start_capture(video)
                        tracking = False

                if self.config["headless"] is False:
                    pulse_rate_pk_pk = self.pulse_rate_bpm_pk_pk if isinstance(self.pulse_rate_bpm_pk_pk, str) else round(
                        self.pulse_rate_bpm_pk_pk, 2)
                    pulse_rate_fft = self.pulse_rate_bpm_fft if isinstance(self.pulse_rate_bpm_fft, str) else round(
                        self.pulse_rate_bpm_fft, 2)
                    cv2.putText(self.last_frame, "HR: PkPk:{} - FFT:{} Frame: {}. Total Frames: {}".
                                format(pulse_rate_pk_pk, pulse_rate_fft, self.frame_number, self.total_frames_read),
                                (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    cv2.imshow('Frame', self.last_frame)

                if self.frame_number > self.config["pulse_sample_frames"]:
                    fps = video.get_actual_fps() if video_file_or_camera == 0 else video.get_frame_rate()
                    self.__update_results(fps, video)
                    self.logger.info("Processing time: {} seconds. FPS: {}. Frame count: {}".
                                     format(round(time.time() - self.start_process_time, 2),
                                            round(self.frame_number / (time.time() - self.start_process_time), 2),
                                            self.frame_number))
                    if self.config["pause_between_samples"] and self.config["headless"] is False:
                        input("Hit enter to continue")
                    self.__start_capture(video)
                    tracking = False
                if self.config["headless"] is False:
                    # Allow UI
                    key = cv2.waitKey(10) & 0xFF
                    if key == ord('q'):
                        break  # Exit
                    elif key == ord('g'):
                        self.config["show_pulse_charts"] = True if self.config["show_pulse_charts"] is False else True
            else:
                self.logger.info("Video stream ended")
                break
        return

    def __update_results(self, actual_fps, video):
        """Process the the inter-fame changes, and filter results in both time and frequency domain """
        result_summary = {
            "passCount": self.hr_estimate_count + 1,
            "trackers": {},
            "fps": actual_fps,
            "video_name": video.video_file_or_camera_name
        }

        # check for a valid ground_truth HR is available. If so store it in the summary
        if self.ground_truth is not None:
            ground_truth_for_period = self.ground_truth.get_average_for_period_ending(
                self.total_frames_read, self.config["pulse_sample_frames"], actual_fps)
            result_summary.update({"groundTruth": round(ground_truth_for_period, 2)})

        self.hr_estimate_count += 1

        index = 1
        for tracker in self.tracker_list:
            tracker.process(actual_fps, self.config["low_pulse_bpm"], self.config["high_pulse_bpm"])
            tracker.calculate_bpm_from_peaks_positive( self.config["low_pulse_bpm"], self.config["high_pulse_bpm"])
            tracker.calculate_bpm_from_fft()

            if tracker.bpm_pk_pk is not None:
                result_summary["trackers"].update({COLOR_PKPK: round(tracker.bpm_pk_pk, 2)})
            if tracker.bpm_fft is not None:
                result_summary["trackers"].update({COLOR_FFT: round(tracker.bpm_fft, 2)})
                result_summary["trackers"].update({CONFIDENCE: round(tracker.bpm_fft_confidence, 2)})

            if self.config["show_pulse_charts"] is True and self.config["headless"] is False:
                self.hr_charts.update_chart(tracker)
            index += 1

        if self.tracker_list[0].bpm_pk_pk is not None:
            self.pulse_rate_bpm_pk_pk = self.tracker_list[0].bpm_pk_pk
        else:
            self.pulse_rate_bpm_pk_pk = "N/A"

        if self.tracker_list[0].bpm_fft is not None:
            self.pulse_rate_bpm_fft = self.tracker_list[0].bpm_fft
        else:
            self.pulse_rate_bpm_fft = "N/A"

        if self.config["csv_output"] is True:
            self.csv_reporter.report_results(result_summary)
        if self.config["http_output"] is True:
            self.http_reporter.report_results(result_summary)

        self.logger.info("Results: {} ".format(result_summary))

    def __round(self, value, precision=2):
        return None if value is None else round(value, precision)

    def __create_trackers(self):
        self.tracker_list.clear()
        self.tracker_list.append(ROIColorICA(self.logger, self.config, 'Color', "color"))

    def __create_camera(self, video_file_or_camera, fps, width, height):
        """Create the appropriate class using opencv or the raspberry Pi piCamera"""
        # For files nor non raspberry pi devices, use opencv, for real-time video on raspberry pi, use CameraRaspbian
        if os.path.isfile("/etc/rpi-issue") and video_file_or_camera == 0:
            return RaspberianGrabber(cv2, fps, width, height, self.logger, video_file_or_camera)
        else:
            return FrameGrabber(cv2, fps, width, height, self.logger, video_file_or_camera)

    def __process_ground_truth(self, video_file_or_camera):
        if video_file_or_camera != 0:
            # processing a video file, check to see if there is an existing ground_truth file
            # noinspection PyPep8
            try:
                folder = os.path.dirname(video_file_or_camera)
                ground_truth_file = "{}/ground_truth.txt".format(folder)
                ground_truth = GroundTruth(self.logger, ground_truth_file)
                ground_truth.process_ground_truth(int(self.config["pulse_sample_frames"] / self.config["video_fps"]))
                self.ground_truth = ground_truth
            except:
                e = sys.exc_info()[0]
                self.logger.error("Exception: {} ".format(e))
