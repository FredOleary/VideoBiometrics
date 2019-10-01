# Measuring pulse rate by analysing micro changes in head motion
The **collector** estimates pulse rate from a video stream by measuring face micro motion. It uses the open source vision library, opencv, to process video streams

## Pre-requisites (Mac Laptop)
1. Python 3 installed (3.7 version minimum)
2. Webcam

## Pre-requisites RaspberryPi
1. Raspberry Pi 3b+
2. Raspberry Pi camera. (picamera) (USB cameras are not supported )
3. Python 3 installed (3.5 version minimum)


## Software installation steps
1. `cd VideoBiometrics/collector`
2. `python3 -m venv venv`  (Create a virtual environment)
3. `source venv/bin/activate` (Activate virtual environment)
4. Install the following python packages
    1. `pip install opencv-contrib-python`
    2. `pip install matplotlib`
    3. `pip install scipy`
    4. `pip install requests`
    
### For the raspberry pi do the additional:
1.`sudo apt-get install at-spi2-core` (remove errors about “org.freedesktop.DBus.Error)

2.`pip install picamera`
    
    
## Usage
1. To verify the installation and camera: `python play_video.py` Verify that video streams and that the camera is correctly positioned for face detection. To exit, move focus to the video window and press 'q'.

2. To measure pulse rate run `python main.py`. Heart rate will be estimated every 10 seconds. Results are stored, (optionally) in a csv file and/or sent to a remote server
3. Optionally use `python main.py video_file.mov` to process an existing video file

## Options
The configuration file config.txt contains the many options for saving heart rate data as well as for development. Config.txt is organized as a python 
dictionary so take care when editing. The one entry that is deployment sensitive is `"server_url"`. If heart results are being sent to a remote server, ensure the service is running

