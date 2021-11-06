# import the necessary packages
from picamera import PiCamera
import time

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.start_preview()
time.sleep(5)
camera.capture('/home/pi/Workspace/image.jpg')
camera.stop_preview()
