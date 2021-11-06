import RPi.GPIO as GPIO
import time
import datetime
from picamera import PiCamera
import requests

picam = PiCamera()
picam.framerate = 10
picam.resolution = (1024, 768)
picam.rotation = 180
# warm camera
picam.start_preview()
time.sleep(10)

GPIO.cleanup()
picam.stop_preview()