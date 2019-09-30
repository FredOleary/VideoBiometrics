import sys
import time
import os
import cv2
import logging

from frame_grabber import FrameGrabber
from raspberian_grabber import RaspberianGrabber

CONFIG_FILE = "config.txt"
LOG_FILE = "play_video.txt"
LOG_LEVEL = logging.DEBUG

# noinspection PyPep8
def play_video(config, video_file_or_camera, logger):
    logger.info("play_video")

    if video_file_or_camera is None:
        video_file_or_camera = 0  # First camera

    video = create_camera(video_file_or_camera, config["video_fps"], config["resolution"]["width"],
                          config["resolution"]["height"], logger)

    is_opened = video.open_video(video_file_or_camera)
    if not is_opened:
        logger.error("Error opening video stream or file, '" + str(video_file_or_camera) + "'")
    else:

        width, height = video.get_resolution()
        config["resolution"]["width"] = width
        config["resolution"]["height"] = height
        config["video_fps"] = video.get_frame_rate()

        logger.info("Video: Resolution = " + str(config["resolution"]["width"]) + " X "
              + str(config["resolution"]["height"]) + ". Frame rate = " + str(round(config["video_fps"])))

    frame_count = 0
    start_time = time.time()
    video.start_capture(-1)
    while video.is_opened():
        ret, frame = video.read_frame()
        if ret:
            frame_count = frame_count + 1
            cv2.putText(frame, "Frame: {}. FPS: {}".format(frame_count, round(frame_count / (time.time() - start_time), 2)),
                        (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            cv2.imshow('Video', frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            break

    end_time = time.time()
    logger.info("Elapsed time: " + str(round(end_time - start_time)) + " seconds. fps:" + str(
        round(frame_count / (end_time - start_time), 2)))
    cv2.destroyAllWindows()
    # When everything done, release the video capture object
    video.close_video()


def read_config():
    with open(CONFIG_FILE, 'r') as config:
        dict_from_file = eval(config.read())
    return dict_from_file


def create_camera(video_file_or_camera, fps, width, height, logger):
    # For video files nor non raspberry pi devices, use open cv, for real-time video on raspberry pi, use CameraRaspbian
    if os.path.isfile("/etc/rpi-issue") and video_file_or_camera == 0 :
        return RaspberianGrabber(cv2, fps, width, height, logger)
    else:
        return FrameGrabber(cv2, fps, width, height, logger)


def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(filename)s:%(funcName)s:%(lineno)d - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(LOG_FILE, mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

def main(args):
    video_file = None
    logger = setup_custom_logger("TEST_VIDEO")
    config = read_config()
    if len(args) > 1:
        video_file = args[1]
    play_video(config, video_file, logger)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
