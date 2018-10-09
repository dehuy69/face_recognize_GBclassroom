import requests
import json
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
#camera setup
camera = PiCamera()
rawCapture = PiRGBArray(camera)
privious_data = []
privious_time = 0
camera.start_preview(fullscreen=False, window=(100,20,480,320))
#server address
addr = 'http://localhost:5000'
test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}
for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
    try:
        img = rawCapture.array
        # encode image as jpeg
        _, img_encoded = cv2.imencode('.jpg', img)
        # send http request with image and receive response
        response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
        # decode response
        print (response)
        print (json.loads(response.text))
    except:
        camera.stop_preview()
        break


# expected output: {u'message': u'image received. size=124x124'}