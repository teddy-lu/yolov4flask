import base64
import io
import json
import os

import requests

# print(os.environ)
# exit()


# Define the endpoint with the format: http://localhost:8501/v1/models/MODEL_NAME:predict
endpoint = "http://127.0.0.1:8555/api/predict"

# Prepare the data that is going to be sent in the POST request
img_dir = '/home/teddy/PycharmProjects/label_yes_voc/JPEGImages/VID_20211011_152628_00060.jpg'
f = open(img_dir, 'rb')
b64data = base64.b64encode(f.read())
f.close()
json_data = {
    "imgb64": b64data.decode('utf-8')
}

# Send the request to the Prediction API
response = requests.post(endpoint, json=json_data, headers={"content-type": "application/json"})

json_response = json.loads(response.text)
print(json_response)
