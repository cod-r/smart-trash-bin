import requests


def get_prediction(path):
    # TODO call prediction api
    url = 'http://192.168.1.168:8080/prediction'
    files = {'file': (open(path, 'rb'))}
    response = requests.post(url, files=files)
    print(response.json())
    return response.json()


get_prediction('image.jpg')
