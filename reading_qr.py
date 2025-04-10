import cv2
import json
import numpy as np
import requests
import urllib



URL = "https://hackattic.com/challenges/reading_qr/"
PARAMS = {'access_token': "90fabb2a44afba20"}
r = requests.get(url = URL+"problem", params = PARAMS)
data = r.json()
img_url = data['image_url']

resp = urllib.request.urlopen(img_url)
arr = np.asarray(bytearray(resp.read()), dtype="uint8")

img = cv2.imdecode(arr, -1)

det=cv2.QRCodeDetector()
val, pts, st_code=det.detectAndDecode(img)
# print(val)

result = {"code":val}

res = requests.post(url=URL+"solve", params = PARAMS, data=json.dumps(result))
print(res.text)

# cv2.imshow('test', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()