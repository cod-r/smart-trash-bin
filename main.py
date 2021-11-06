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
time.sleep(2)

CUVA_NEUTRAL = 5
CUVA_DOWN = 10

# tevusca 4 pozitii
TEVUSCA_NEUTRAL = 7.5
TEVUSCA_RIGHT_90 = 12.5
TEVUSCA_LEFT_90 = 3.7
TEVUSCA_LEFT_180 = 0.000001

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


# # quick test cuva
# cuva.ChangeDutyCycle(CUVA_DOWN)
# time.sleep(2)
# cuva.ChangeDutyCycle(CUVA_NEUTRAL)
# time.sleep(20)

# quick test tevusca
# tevusca.ChangeDutyCycle(TEVUSCA_LEFT_90)
# time.sleep(2)
# tevusca.ChangeDutyCycle(TEVUSCA_RIGHT_90)
# time.sleep(2)
# tevusca.ChangeDutyCycle(TEVUSCA_LEFT_180)
# time.sleep(2)
# tevusca.ChangeDutyCycle(TEVUSCA_NEUTRAL)
# time.sleep(2)


def capture_image(path):
    picam.capture(path, use_video_port=True)


def get_prediction(path):
    url = 'http://192.168.1.168:8080/prediction'
    files = {'file': (open(path, 'rb'))}
    response = requests.post(url, files=files)
    print(response.json())
    return response.json()


try:
    while True:
        time.sleep(5)
        print('loop')
        date_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
        image_path = '/home/pi/image_' + date_time + '.jpg'
        capture_image(image_path)
        prediction = get_prediction(image_path)

        if prediction == 'GLASS':
            tevusca.ChangeDutyCycle(TEVUSCA_LEFT_90)
            time.sleep(2)
            # Empty cuva
            cuva.ChangeDutyCycle(CUVA_DOWN)
            time.sleep(2)
            cuva.ChangeDutyCycle(CUVA_NEUTRAL)
            print('sticla deployed')
            tevusca.ChangeDutyCycle(TEVUSCA_NEUTRAL)

        elif prediction == 'PAPER':
            tevusca.ChangeDutyCycle(TEVUSCA_RIGHT_90)
            time.sleep(2)
            # Empty cuva
            cuva.ChangeDutyCycle(CUVA_DOWN)
            time.sleep(2)
            cuva.ChangeDutyCycle(CUVA_NEUTRAL)
            print('hartie deployed')
            tevusca.ChangeDutyCycle(TEVUSCA_NEUTRAL)

        elif prediction == 'WASTE':
            tevusca.ChangeDutyCycle(TEVUSCA_NEUTRAL)
            time.sleep(2)
            # Empty cuva
            cuva.ChangeDutyCycle(CUVA_DOWN)
            time.sleep(2)
            cuva.ChangeDutyCycle(CUVA_NEUTRAL)
            print('menajer deployed')
            tevusca.ChangeDutyCycle(TEVUSCA_NEUTRAL)

        elif prediction == 'PLASTIC':
            tevusca.ChangeDutyCycle(TEVUSCA_LEFT_180)
            time.sleep(2)
            # Empty cuva
            cuva.ChangeDutyCycle(CUVA_DOWN)
            time.sleep(2)
            cuva.ChangeDutyCycle(CUVA_NEUTRAL)
            print('plastic deployed')
            tevusca.ChangeDutyCycle(TEVUSCA_NEUTRAL)

        elif prediction == 'NOTHING':
            print('nothing')


except KeyboardInterrupt:
    print("Terminated by pressing CTRL+C ")
finally:
    GPIO.cleanup()
    picam.close()
    picam.stop_preview()
