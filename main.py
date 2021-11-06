import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import picamera.array

CUVA_NEUTRAL = 5
CUVA_DOWN = 0.000001

TEVUSCA_NEUTRAL = 5
TEVUSCA_LEFT_90 = 0.000001
TEVUSCA_RIGHT_90 = 9

picam = PiCamera()
picam.framerate = 10
picam.resolution = (320, 240)
picam.rotation = 180

GPIO.setmode(GPIO.BCM)
servoTevusca = 12
servoCuva = 13
GPIO.setup(servoTevusca, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(servoCuva, GPIO.OUT, initial=GPIO.LOW)

tevusca = GPIO.PWM(servoTevusca, 50)  # GPIO 12, PWM 50Hz
cuva = GPIO.PWM(servoCuva, 50)  # GPIO 13, PWM 50Hz
tevusca.start(TEVUSCA_NEUTRAL)
cuva.start(CUVA_NEUTRAL)
time.sleep(2)

# quick test
tevusca.ChangeDutyCycle(TEVUSCA_LEFT_90)
time.sleep(2)
tevusca.ChangeDutyCycle(TEVUSCA_RIGHT_90)
time.sleep(2)
tevusca.ChangeDutyCycle(TEVUSCA_NEUTRAL)
time.sleep(2)


def capture_image():
    raw_capture = picamera.array.PiRGBArray(picam)
    picam.capture(raw_capture, format='rgb', use_video_port=True)
    img = raw_capture.array.astype('uint8')

    return img


def get_prediction(image):
    # TODO call prediction api
    return 'prediction'


try:
    while True:
        image = capture_image()
        prediction = get_prediction(image)

        if prediction == 'sticla':
            print('sticla')
            tevusca.ChangeDutyCycle(TEVUSCA_LEFT_90)
            time.sleep(2)
            # Empty cuva
            cuva.ChangeDutyCycle(CUVA_DOWN)
            time.sleep(2)
            cuva.ChangeDutyCycle(CUVA_NEUTRAL)
            print('sticla deployed')

        elif prediction == 'hartie':
            print('hartie')
            tevusca.ChangeDutyCycle(TEVUSCA_RIGHT_90)
            time.sleep(2)
            # Empty cuva
            cuva.ChangeDutyCycle(CUVA_DOWN)
            time.sleep(2)
            cuva.ChangeDutyCycle(CUVA_NEUTRAL)
            print('hartie deployed')

        elif prediction == 'menajer':
            print('menajer')
            tevusca.ChangeDutyCycle(TEVUSCA_NEUTRAL)
            time.sleep(2)
            # Empty cuva
            cuva.ChangeDutyCycle(CUVA_DOWN)
            time.sleep(2)
            cuva.ChangeDutyCycle(CUVA_NEUTRAL)
            print('menajer deployed')


except KeyboardInterrupt:
    print("Terminated by pressing CTRL+C ")
finally:
    GPIO.cleanup()
    picam.close()
