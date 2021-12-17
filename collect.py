import time

import cv2
import time

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3, 800)
    cap.set(4, 800)
    print("曝光度：", cap.get(cv2.CAP_PROP_EXPOSURE))  # 166.0
    print("亮度：", cap.get(cv2.CAP_PROP_BRIGHTNESS))  # 0.0
    print("对比度：", cap.get(cv2.CAP_PROP_CONTRAST))  # 50.0
    print("饱和度：", cap.get(cv2.CAP_PROP_SATURATION))  # 64.0
    print("色调：", cap.get(cv2.CAP_PROP_HUE))  # 0.0

    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # 自动模式
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # 手动模式
    cap.set(cv2.CAP_PROP_EXPOSURE, 100)  # 设置曝光
    # cap.set(cv2.CAP_PROP_BRIGHTNESS, 0)
    # cap.set(cv2.CAP_PROP_CONTRAST, 50)
    # cap.set(cv2.CAP_PROP_SATURATION, 64)
    # cap.set(cv2.CAP_PROP_HUE, 0)

    while cap.isOpened():
        ret_flag, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow("video", frame)
        k = cv2.waitKey(200)
        print(k)
        if k == 27:
            break
        elif k == 13:
            print(time.time() // 1)
            cv2.imwrite("data/{:d}.jpg".format(int(time.time())), frame)
    cap.release()
    cv2.destroyAllWindows()
