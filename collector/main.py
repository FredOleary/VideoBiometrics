import sys
import typing
from frame_processor import FrameProcessor
import logging

CONFIG_FILE = "config.txt"
LOG_LEVEL = logging.DEBUG
LOG_FILE = "collector.txt"


def read_config():
    """Read the config.txt file. This is formatted as a python dictionary"""
    with open(CONFIG_FILE, 'r') as config:
        dict_from_file = eval(config.read())
    return dict_from_file


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


def main(args: typing.List[str]) -> int:
    """Analyse video file or camera for motion. If no file is entered, the first camera is used."""
    video_file = None
    config = read_config()
    logger = setup_custom_logger("COLLECTOR")
    logger.info("Application started")

    frame_processor = FrameProcessor(config, logger)
    if len(args) > 1:
        video_file = args[1]
    frame_processor.capture(video_file)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
