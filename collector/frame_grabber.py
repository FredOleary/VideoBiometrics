import time
from threading import Thread
import queue


class FrameGrabber:

    def __init__(self, cv2, fps, width, height, logger):
        self.cv2 = cv2
        self.fps = fps
        self.width = width
        self.height = height
        self.logger = logger
        self.capture = None
        self.stopped = True
        self.paused = True
        self.frame_queue = queue.Queue()
        self.start_time = time.time()
        self.end_time = time.time() + 1
        self.total_frame_count = 0
        self.video_ended = False
        self.is_live_stream = False

    def set_frame_rate(self, fps):
        self.capture.set(self.cv2.CAP_PROP_FPS, fps)

    def set_resolution(self, width, height):
        self.capture.set(self.cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(self.cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame_rate(self):
        return self.capture.get(self.cv2.CAP_PROP_FPS)

    def get_actual_frame_rate(self):
        return self.total_frame_count / (time.time() - self.start_time)

    def get_resolution(self):
        width = self.capture.get(self.cv2.CAP_PROP_FRAME_WIDTH)
        height = self.capture.get(self.cv2.CAP_PROP_FRAME_HEIGHT)
        return width, height

    def open_video(self, video_file_or_camera):
        if type(video_file_or_camera) is int:
            self.is_live_stream = True
        self.capture = self.cv2.VideoCapture(video_file_or_camera)
        self.capture.set(self.cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(self.cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.capture.set(self.cv2.CAP_PROP_FPS, self.fps)
        is_opened = self.capture.isOpened()
        if is_opened:
            self.stopped = False
            thread = Thread(target=self.__update, args=())
            thread.setDaemon(True)
            thread.start()

        return self.capture.isOpened()

    def close_video(self):
        self.logger.info("Closing video")
        if not self.video_ended:
            self.end_time = time.time()
        self.stopped = True
        time.sleep(0.3)

    def is_opened(self):
        return self.capture.isOpened() or self.frame_queue.qsize() > 0

    def read_frame(self):
        while True:
            if self.frame_queue.qsize() > 0:
                return True, self.frame_queue.get()
            elif self.video_ended:
                return False, None
            else:
                time.sleep(0.10)

    def start_capture(self, number_of_frames):
        # For video files, keep the current queue. For live video, restart it
        if self.is_live_stream:
            self.frame_queue = queue.Queue()
        self.frame_number = 0
        self.number_of_frames = number_of_frames
        self.paused = False
        self.start_time = time.time()


    def __update(self):
        self.total_frame_count = 0
        while not self.stopped:
            if not self.paused:
                ret, frame = self.capture.read()
                if ret:
                    self.total_frame_count += 1
                    self.frame_queue.put(frame)
                    self.frame_number += 1
                    if self.frame_number >= self.number_of_frames and self.number_of_frames != -1:
                        self.paused = True
                        self.end_time = time.time()
                        self.logger.info("Paused. Total frame count: {}, FPS: {}".format(
                            self.total_frame_count,
                            round(self.frame_number / (self.end_time - self.start_time), 2)))
                else:
                    if not self.video_ended:
                        self.video_ended = True
                        self.end_time = time.time()

                    self.logger.info("Frame Queue size: ", self.frame_queue.qsize())
                    self.stopped = True
            else:
                time.sleep(0.10)

        self.logger.info("Video Ended. Frame Count: {}".format(self.total_frame_count))
        self.capture.release()
        return
