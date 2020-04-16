# @Author: Olivier Watte <user>
# @Date:   2020-04-15T09:00:46-04:00
# @Email:  owatte@biolo.tech
# @Last modified by:   user
# @Last modified time: 2020-04-16T17:22:13-04:00
# @License: GPLv3
# @Copyright: Biolotech
"""
This module is part code of Mr Hackquarium DIY trap-cam using a Raspberry pi
with a pi camera and PIR sensor.
This module is based on  python picamera.

Run
    $ python3 trapcam.py

Parameters
    All parameters are in the top of the script.
    See picamera doc for more options: https://picamera.readthedocs.io

TODO 
    * Real module with config file to publish on pypi
    * Docker version
"""
import time
from datetime import datetime
import locale
import picamera
import RPi.GPIO as GPIO

PIRSENSOR_GPIO = 24
LOCALE = 'fr_FR.UTF-8'
ANNOTATION_STRFTIME = '%-d %B %Y %H:%M'

RECORD_MODE = 'video'  # set type as 'video' or 'picture'
VIDEO_DURATION = 30  # duration in sec
VIDEO_ANNOTATION = True  # show text with date on capture
VIDEO_FORMAT = 'h264'  # set type as 'h264' or 'mjpeg'
VIDEO_RESOLUTION = (1296, 972)  # (1920, 1080), (640, 480) ...
PICTURE_FORMAT = 'png'  # set type as 'jpeg', 'png', 'gif', 'bmp' ...
PICTURE_RESOLUTION = (1296, 972)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIRSENSOR_GPIO, GPIO.IN)
locale.setlocale(locale.LC_TIME, LOCALE)


def set_filename(ext):
    ''' Set filename based on capture time YYYYMMDD '''

    nowtime = now.strftime('%Y%m%d%-H%M%S')
    filename = "trapcam_{nowtime}.{ext}".format(nowtime=nowtime, ext=ext)
    return filename


while True:
    if GPIO.input(PIRSENSOR_GPIO):
        print("Intruder detected")
        now = datetime.now()
        if RECORD_MODE == 'video':
            filename = set_filename(VIDEO_FORMAT)
            print(filename)
            with picamera.PiCamera() as camera:
                camera.resolution = VIDEO_RESOLUTION
                camera.annotate_background = picamera.Color('black')
                camera.annotate_text = now.strftime(VIDEO_ANNOTATION_STRFTIME)
                camera.start_recording(filename, format=VIDEO_FORMAT)
                camera.wait_recording(VIDEO_DURATION)
                camera.stop_recording()
        elif RECORD_MODE == 'picture':
            filename = set_filename(PICTURE_FORMAT)
            print(filename)
            with picamera.PiCamera() as camera:
                camera.resolution = VIDEO_RESOLUTION
                camera.start_preview()
                time.sleep(2)
                camera.annotate_text = now.strftime(VIDEO_ANNOTATION_STRFTIME)
                camera.capture(filename, format=PICTURE_FORMAT)
    time.sleep(0.1)
