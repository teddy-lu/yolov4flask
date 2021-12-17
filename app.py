import json

from flask import Flask, jsonify, request

import predict

app = Flask(__name__)
# 防止jsonify把数据格式化后排序
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def hello_world():
    return {"message": "Hello AI World!"}


@app.route('/api/predict', methods=['POST'])
def predict_img():
    if request.method != "POST":
        return jsonify({"error": "dd"})
    data = request.get_data().decode('utf-8')
    imgb64 = json.loads(data)['imgb64']
    res = predict.dect(imgb64)
    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8555, debug=True)
