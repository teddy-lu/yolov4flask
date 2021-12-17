import time

import cv2
import numpy as np

model_label = r'./cfg/obj.names'
cfgFile = "./cfg/yolov4-tiny-custom.cfg"
darknetModel = './cfg/yolov4-tiny-custom_best.weights'
LABELS = open(model_label).read().strip().split('\n')
num_class = len(LABELS)

np.random.seed(28)
COLORS = np.random.randint(0, 255, size=(num_class, 3), dtype='uint8')

if __name__ == '__main__':
    cap = cv2.VideoCapture(2)
    cap.set(3, 900)
    cap.set(4, 900)
    net = cv2.dnn.readNetFromDarknet(cfgFile=cfgFile, darknetModel=darknetModel)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    while cap.isOpened():
        ret_flag, v_show = cap.read()
        frame = cv2.flip(v_show,1)

        (H, W) = frame.shape[:2]

        ln = net.getLayerNames()
        ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()
        boxes = []
        confidences = []
        classIDs = []
        # 置信度大于.5的边界框数据保留下来
        confidence_thre = 0.5
        # 非最大抑制的阈值。
        nms_thre = 0.3

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > confidence_thre:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_thre, nms_thre)

        data = {"counts": len(idxs), "msg": "本次检测话费了{:.2f}秒来预测一张图片".format(end - start)}
        listLayer = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # 画出来
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = '{}: {:.3f}'.format(LABELS[classIDs[i]], confidences[i])
                (text_w, text_h), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                cv2.rectangle(frame, (x, y - text_h - baseline), (x + text_w, y), color, -1)
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                info = {
                    "label": LABELS[classIDs[i]],
                    "scores": confidences[i],
                    "x": str(x),
                    "y": str(y),
                    "w": str(w),
                    "h": str(h),
                }
                listLayer.append(info)

        data["data"] = listLayer
        print(data)
        cv2.imshow("video", frame)
        k = cv2.waitKey(100)
        if k == 27:
            break
    cv2.destroyAllWindows()