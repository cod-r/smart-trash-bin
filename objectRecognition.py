import io
import os
import time

from picamera import PiCamera
from google.cloud import vision

class ObjectRecognition:
    def getImageLabels(self, imageName):

        # Instantiates a client
        client = vision.ImageAnnotatorClient()

        # The name of the image file to annotate
        file_name = os.path.abspath(imageName)

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        return labels

    def isGlass(self, labels):
        glassLabels = ['Glass', 'Glass bottle']
        for label in labels:
            if (label.description in glassLabels):
                return 1
        return 0

    def isPlastic(self, labels):
        plasticLabels = ['Plastic', 'Plastic bottle']
        for label in labels:
            if (label.description in plasticLabels):
                return 1
        return 0

camera = PiCamera()
camera.start_preview()
time.sleep(5)
camera.capture('/home/pi/Workspace/image.jpg')
camera.stop_preview()

objectRecognition = ObjectRecognition()
labels = objectRecognition.getImageLabels('/home/pi/Workspace/image.jpg')
print('Labels:')
for label in labels:
    print(label.description)

isGlass = objectRecognition.isGlass(labels)
isPlastic = objectRecognition.isPlastic(labels)

print('glass?')
print(isGlass)
print('plastic?')
print(isPlastic)