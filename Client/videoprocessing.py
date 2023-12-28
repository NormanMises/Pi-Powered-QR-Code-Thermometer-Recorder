import time

import cv2
from QRcode_creat import flag_list

def gen(camera):
    while True:
        img = camera.get_frame()
        ret, jpeg = cv2.imencode('.jpg', img)
        # 对图像进行编码输出
        yield b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n'


class VideoCamera(object):
    def __init__(self, path):
        self.path = path
        # 打开一个视频源
        # print(f'{cv2.CAP_PROP_BUFFERSIZE}, {cv2.CAP_PROP_FRAME_WIDTH}, {cv2.CAP_PROP_FRAME_HEIGHT}, {cv2.CAP_PROP_FPS}, ')
        self.cap = cv2.VideoCapture(int(self.path))
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.QR_detector = cv2.QRCodeDetector()
        self.id = '-1'
        self.flag_list = flag_list
        print(self.flag_list)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        self.id = '-1'
        # try:
        cnt = 0
        while True:
            success, img = self.cap.read()
            if not success:
                # print('error input')
                continue

            if cnt < 1:
                cnt += 1
                continue

            # cv2.imshow("img", img)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            # st = time.time()
            # 二维码检测
            flag_now, _, QR = self.QR_detector.detectAndDecode(img)
            if flag_now in self.flag_list:
                self.id = flag_now
                break
                # return QR
            # ed = time.time()
            # print(f'{st}, {ed}, {ed - st}')

            # return img
        # if flag_now == flag_pass:
        #     continue
        # flag_pass = flag_now
        #
        # if flag_pass in flag_list:
        #     pass

    # except:
    #     print('\n Ctrl + C QUIT')
    #
    # finally:
    #     cap.release()
