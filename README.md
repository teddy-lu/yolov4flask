# yolov4flask


首先安装好docker

[安装docker](https://yeasy.gitbook.io/docker_practice/install/ubunt)

Linux 部署
首先预训练yolo，得到训练后的 权重文件，统一命名为yolo-obj.weights，并同时把训练的obj.names,yolov4.cfg文件放入本项目cfg下替换掉原来的文件，cfg目录结构如下

为方便构建 建议自行下载opencv4.5的zip包 和python3.8的tgz以上的包在本项目根目录

```shell
├── cfg
│   ├── yolov4.cfg
│   ├── obj.names
│   └── yolo-obj.weights
```

构建方法一(本地)：含测试文件

```shell
# 定位到项目根目录，如果使用虚拟环境 conda或者venv之类的可以自行启动，后安装依赖
pip install -r requirements.txt

# 启动本地服务，两种启动方式
flask run
python app.py

# 启动服务成功后，就可以根据启动服务的端口，修改好测试文件的端口
python test_img.py

# 之后就会得到返回的json数据，和在out目录下查看到本次检测的图像结果
```

构建方法二(Docker 服务端)：基于Dockerfile构建

```shell
# 创建镜像
docker build -t yolo_flask_image -f Dockerfile .

# 创建容器
docker run -d --name yolo_flask -p 8555:8555 yolo_flask_image

# 创建可查看验证结果容器
docker run -d --name yolo_flask \                         
 --mount type=bind,source=/tmp/out,target=/home/yolo_serv/out \
 -p 8555:8555 yolo_flask_image

# 验证是否运行成功
curl GET http://localhost:8555/
{"message": "Hello World!"}

# 查看日志
docker logs -f [container_id]

# 现在加入了docker-compose文件，也可以通过使用命令启动
cp .env.example .env

# 基于CPU的构建
docker-compose -f docker-compose.yml up --build -d
# 基于GPU的构建
docker-compose -f docker-compose-gpu.yml up --build -d
# 查看GPU实时调用情况
watch -n 0.1 -d nvidia-smi
```

客户端如何调用接口进行检测呢？目前定义接口传递base64图片数据，进行检测。这里是调用例子
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

接口将返回json数据给客户端
```json
{
	'counts': 15, // 被标记的数量
	'data': [{
		'label': 'yes', // 被标记的分类
		'scores': 0.9960584044456482, // 标记的分数
		'x': '44', // 被标记的边界坐标x
		'y': '191', // 被标记的边界坐标y
		'w': '44', // 宽
		'h': '100' // 高
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