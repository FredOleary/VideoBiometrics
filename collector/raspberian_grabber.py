import time
import queue
from threading import Thread

try:
    # noinspection PyUnresolvedReferences
    from picamera.array import PiRGBArray
    # noinspection PyUnresolvedReferences
    from picamera import PiCamera
    # noinspection PyUnresolvedReferences
    from picamera import PiCameraMMALError
except ImportError:
    print("Not raspberry Pi")


class RaspberianGrabber:
    def __init__(self, cv2, fps, width, height, logger):
        self.camera = None
        self.fps = fps
        self.width = width
        self.height = height
        self.logger = logger
        self.is_open = False
        self.stream = None
        self.stopped = False
        self.rawCapture = None
        self.paused = True
        self.frame_queue = queue.Queue()
        self.start_time = time.time()
        self.total_frame_count = 0
        self.is_live_stream = True # This camera is used only for live video

    def set_frame_rate(self, fps):
        self.camera.framerate = fps

    def set_resolution(self, width, height):
        self.camera.resolution = (width, height)
        self.rawCapture = PiRGBArray(self.camera, size=(width, height))

    def get_frame_rate(self):
        return self.camera.framerate

    def get_resolution(self):
        width, height = self.camera.resolution
        return width, height


    def open_video(self, video_file_or_camera):
        try:
            self.camera = PiCamera()
            self.camera.resolution = (self.width, self.height)
            self.camera.framerate = self.fps
            self.rawCapture = PiRGBArray(self.camera, size=(self.width, self.height))
            self.stream = self.camera.capture_continuous(self.rawCapture,
                                                         format="bgr", use_video_port=True)
            self.stopped = False
            self.is_open = True
            thread = Thread(target=self.__update, args=())
            thread.setDaemon(True)
            thread.start()
            # allow the camera to warm up
            time.sleep(0.3)
            return True
        except PiCameraMMALError:
            self.logger.error("Open camera failed")
            self.is_open = False
            return False

    def close_video(self):
        self.is_open = False
        self.stopped = True
        time.sleep(0.3)

    def is_opened(self):
        return self.is_open or self.frame_queue.qsize() > 0

    def read_frame(self):
        return True, self.frame_queue.get()     # Block until next frame is delivered

    def start_capture(self, number_of_frames):
        # self.logger.info("Total frame count: {}".format(self.total_frame_count))
        self.frame_queue = queue.Queue()
        self.frame_number = 0
        self.number_of_frames = number_of_frames
        self.paused = False
        self.start_time = time.time()

    def get_actual_fps(self):
        return round(self.frame_number / (self.end_time - self.start_time), 2)

    def __update(self):
        self.total_frame_count = 0
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.total_frame_count += 1
            if not self.paused:
                self.frame_queue.put(f.array)
                self.frame_number += 1
                self.end_time = time.time()
                if self.frame_number > self.number_of_frames and self.number_of_frames != -1:
                    self.paused = True
                    fps = round(self.frame_number / (self.end_time - self.start_time), 2)
                    self.logger.info("Paused. Total frame count: {}, FPS: {}".format(
                        self.total_frame_count, fps))

            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                break

        self.logger.info("Video Ended. Frame Count: {}".format(self.total_frame_count))
        return
