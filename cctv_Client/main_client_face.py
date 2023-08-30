# -*- coding: utf-8 -*-
import json
import os
import sys
from typing import List

import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal, QTimer, QTime, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
import time
import requests


''' custom import '''
import def_api_request, def_make_json

# system UI (.ui file)
form_class = uic.loadUiType("ui_client_face.ui")[0]


class MyMainGUI(QMainWindow, form_class, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('systemSW')
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(MyMainGUI):
    whichSignalInt = 1

    def __init__(self, parent=None):
        super().__init__(parent)


        # TImer 시간
        self.textB_Timer.setAlignment(Qt.AlignCenter)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        # Btn
        self.btn_up.clicked.connect(lambda: self.cam_tilt(1))
        self.btn_down.clicked.connect(lambda: self.cam_tilt(2))
        self.btn_left.clicked.connect(lambda: self.cam_tilt(3))
        self.btn_right.clicked.connect(lambda: self.cam_tilt(4))

        self.btn_connect_video_server.clicked.connect(lambda: self.listener_btn_connect_video_server())

        '''     thread 선언부      '''
        '''Thread :: control panel api sender/request'''

        self.th1 = Thread_api_request(parent=self)
        self.th1.signal_api_result.connect(self.slot_api_result)

        self.th2 = Thread_getVideo(parent=self)
        self.th2.signal_video_result.connect(self.slot_video_result)

    ''' 공용 pannel 함수 '''

    # 방향제어 Btn
    def cam_tilt(self, index):
        if index == 1:
            print('1')
            self.api_request(101, 'up')
        elif index == 2:
            print('2')
            self.api_request(101, 'down')
        elif index == 3:
            print('3')
            self.api_request(101, 'left')
        elif index == 4:
            print('4')
            self.api_request(101, 'right')

    def api_request(self, *args):
        if args[0] == 101:
            self.th1.workType = 101
            self.th1.api_type = 'put'
            self.th1.api_url = f'cctv/cctv_move/{args[1]}'
            self.th1.start()

    def slot_api_result(self, workType, data):
        # if workType == 600:
        print(f'Slot : workType : {workType}, data : {data}')

    ''' 동영상 재생 함수 '''

    def listener_btn_connect_video_server(self):
        print('listener')
        self.th2.workType = 201
        self.th2.api_url = 'http://**********'
        self.th2.start()

    def slot_video_result(self, pixmap):
        self.label_video.setPixmap(pixmap)

    # 상단 시간 표현하는 함수
    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.textB_Timer.setText(label_time)
        self.textB_Timer.setAlignment(Qt.AlignCenter)

    # process kill switch (exit button)
    def thread_process_kill(self):
        QCoreApplication.instance().quit()


# api request / self.th6
class Thread_getVideo(QThread):
    signal_video_result = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__()
        self.workType = 0
        self.api_url = ''
        self.api_body = ''

    def run(self):
        print(f'Thread : {self.workType}')
        while True:
            response = requests.get(self.api_url, stream=True)
            if response.status_code != 200:
                print('Error receiving video stream')
                break

            bytes_data = bytes()
            for chunk in response.iter_content(chunk_size=1024):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b + 2]
                    bytes_data = bytes_data[b + 2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = frame_rgb.shape
                    q_image = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_image)
                    # self.video_label.setPixmap(pixmap)

                    self.signal_video_result.emit(pixmap)

        #             cv2.imshow('Client 2 Monitor', frame)
        #             if cv2.waitKey(1) & 0xFF == ord('q'):
        #                 break
        #
        # cv2.destroyAllWindows()


# api request / self.th6
class Thread_api_request(QThread):
    signal_api_result = pyqtSignal(int, object)

    def __init__(self, parent=None):
        super().__init__()
        self.workType = 0
        self.api_type = ''
        self.api_url = ''
        self.api_body = ''

    def run(self):
        print(f'Thread : {self.workType}')
        result = def_api_request.api_request(self.api_type, self.api_url, self.api_body)
        self.signal_api_result.emit(self.workType, result)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
