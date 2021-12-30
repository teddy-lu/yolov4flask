# yolov4flask

First, you have to install docker

[How to install docker](https://yeasy.gitbook.io/docker_practice/install/ubunt)

Deploy with Linux 

Pre-train yolo first and then you will receive a weighting file that is named yolo-obj.weights. At the same time, please place the training obj.names,yolov4.cfg file into this project cfg to substitute the original file, the cfg directory structure is as follows:

```shell
├── cfg
│   ├── yolov4.cfg
│   ├── obj.names
│   └── yolo-obj.weights
```

Building method 1(local): include test

```shell
# At the project root directory, use the command to install dependencies. If you use a virtual environment, you should start the service with conda or venv.
pip install -r requirements.txt

# There are two ways to start the local http service
flask run
python app.py

# After http service has started successfully, you can change the port in file test_img.py according to your service port.
python test_img.py

# you will get the json data after running the command, and you can see the result pics of this test under the directory output.
```

Building method 2(with Docker)：build with Dockerfile

```shell
# create image
docker build -t yolo_flask_image -f Dockerfile .

# create container
docker run -d --name yolo_flask -p 8555:8555 yolo_flask_image

# create the container which can check the result
docker run -d --name yolo_flask \                         
 --mount type=bind,source=/tmp/out,target=/home/yolo_serv/out \
 -p 8555:8555 yolo_flask_image

# use the command to check http service whether worked successful
curl GET http://localhost:8555/
{"message": "Hello World!"}

# check the docker log
docker logs -f [container_id]

# you can also start the docker service such with the file docker-compose.yml by using the command
cp .env.example .env

# build for the cpu
docker-compose -f docker-compose.yml up --build -d
# build for the gpu
docker-compose -f docker-compose-gpu.yml up --build -d
# check the GPU real-time view
watch -n 0.1 -d nvidia-smi
```

So how can our clients use call interface detection? Follow this example and you will get the result.
```python
# Define the endpoint with the format: 
endpoint = "http://localhost:8555/api/predict"

# Prepare the data that is going to be sent in the POST request
img_dir = '/home/teddy/PycharmProjects/label_yes_voc/28210923000000.jpeg'
f = open(img_dir, 'rb')
b64data = base64.b64encode(f.read())
f.close()
json_data = {
    "imgb64": b64data.decode('utf-8')
}

# Send the request to the Prediction API，Only POST method allow
response = requests.post(endpoint, json=json_data, headers={"content-type": "application/json"})
```

This is the example result of json data .
```json
{
	'counts': 15, // marked num
	'data': [{
		'label': 'yes', // marked category
		'scores': 0.9960584044456482, // marked scores
		'x': '44', // marked x axis
		'y': '191', // marked y axis
		'w': '44', // width
		'h': '100' // height
	}, {
	...
    }, {
		'label': 'yes',
		'scores': 0.7002959251403809,
		'x': '1',
		'y': '102',
		'w': '37',
		'h': '201'
	}]
}
```