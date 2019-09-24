import sys
import typing
from frame_processor import FrameProcessor

CONFIG_FILE = "config.txt"


def read_config():
    """Read the config.txt file. This is formatted as a python dictionary"""
    with open(CONFIG_FILE, 'r') as config:
        dict_from_file = eval(config.read())
    return dict_from_file


def main(args: typing.List[str]) -> int:
    """Analyse video file or camera for motion. If no file is entered, the first camera is used."""
    video_file = None
    config = read_config()
    frame_processor = FrameProcessor(config)
    if len(args) > 1:
        video_file = args[1]
    frame_processor.capture(video_file)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
