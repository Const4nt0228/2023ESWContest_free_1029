import queue
from time import sleep
import time
import paho.mqtt.client as mqtt
import cv2
import threading
import numpy as np
import pygame
# import servoTest3
import requests


# import atexit


class face_detector_cam:
    def __init__(self):
        '''
        16:9
        3840x2160 / 640x480 / 960x540 /
        1920x1080 / 1280x720 / 960x540 / 848x480 / 640 x 360
        '''

        # self.servoTest3_instance = servoTest3.servo_module()

        self.detect_2_y = None
        self.detect_2_x = None
        self.detect_1_y = None
        self.detect_1_x = None
        self.sector_arr = None

        self.cam_width = 640
        self.cam_height = 360

        self.server_url = 'http://'

        # sound player
        self.detected = False
        self.detection_timeout = 3
        self.detection_end_time: float = 0
        self.audio_file = "monalisa_3.wav"

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        print(str(rc))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(self, client, userdata, msg):
        msgdata = str(msg.payload.decode("utf-8"))
        print(f'Topic : [{msg.topic}], MSG : [{msgdata}]')
        self.servoTest3_instance.servo_start(msgdata)

    def start_mqtt(self):
        client = mqtt.Client()
        # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_subscribe(topic 구독),
        # on_message(발행된 메세지가 들어왔을 때)
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_subscribe = self.on_subscribe
        client.on_message = self.on_message
        # address : localhost, port: 1883 에 연결
        client.connect('0.0.0.0', 1883)
        # common topic 으로 메세지 발행
        client.subscribe('move')
        client.loop_forever()

    def capture_video(self, frame_buffer, request_event):

        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.cam_width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cam_height)

        width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        print(f'width = {int(width)}, height = {int(height)}')

        self.sector_arr = np.zeros((int(width), int(height)))

        print(self.sector_arr)

        # xml = 'haarcascade_frontalface_default.xml'
        xml = './lib/haarcascades/haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(xml)

        if not capture.isOpened():
            print("Cam doesn't connected")
            exit()

        while capture.isOpened():
            status, frame = capture.read()

            if status:

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.05, 5)

                self.detect_1_x = int(self.cam_width * 3 / 8)
                self.detect_1_y = int(self.cam_height * 1 / 8)
                self.detect_2_x = int(self.cam_width * 5 / 8)
                self.detect_2_y = int(self.cam_height * 7 / 8)

                cv2.rectangle(frame, (self.detect_1_x, self.detect_1_y),
                              (self.detect_2_x, self.detect_2_y), (0, 0, 255), 2)

                if len(faces):
                    for (x, y, w, h) in faces:
                        if (self.detect_1_x <= x <= self.detect_2_x) and (self.detect_1_y <= y <= self.detect_2_y):
                            cv2.rectangle(frame, (x, y, w, h), (255, 0, 0), 3)
                            self.detected = True
                            self.detection_end_time = time.time() + self.detection_timeout
                else:
                    if time.time() > self.detection_end_time:
                        self.detected = False

                frame_buffer[0] = frame.copy()
                request_event.set()

                # _, img_encoded = cv2.imencode('.jpg', frame)
                # response = requests.post(self.server_url, data=img_encoded.tobytes(),
                #                          headers={'Content-Type': 'image/jpeg'})
                cv2.imshow("Video", frame)

                sleep(0.01)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()

    def send_frame_module(self, frame_buffer, request_event):
        while True:
            request_event.wait()
            request_event.clear()

            frame = frame_buffer[0]
            if frame is not None:
                _, img_encoded = cv2.imencode('.jpg', frame)
                response = requests.post(self.server_url, data=img_encoded.tobytes(),
                                         headers={'Content-Type': 'image/jpeg'})

                frame_buffer[0] = None

    def api_req_module(self, frame):
        print()

        try:
            _, img_encoded = cv2.imencode('.jpg', frame)
            response = requests.post(self.server_url, data=img_encoded.tobytes(),
                                     headers={'Content-Type': 'image/jpeg'})

        except requests.exceptions.Timeout as errd:
            print("Timeout Error : ", errd)

        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting : ", errc)

        except requests.exceptions.HTTPError as errb:
            print("Http Error : ", errb)

        # Any Error except upper exception
        except requests.exceptions.RequestException as erra:
            print("AnyException : ", erra)

    def sound_player(self):
        pygame.mixer.init()

        while True:
            if self.detected:
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.play()
                # time.sleep(pygame.mixer.music.get_length())
                while pygame.mixer.music.get_busy():
                    sleep(1)

            sleep(0.1)

    def working(self):

        frame_buffer = [None]
        request_event = threading.Event()

        # video capture
        t1 = threading.Thread(target=self.capture_video, args=(frame_buffer, request_event))
        t1.start()

        mqtt
        t2 = threading.Thread(target=self.start_mqtt)
        t2.start()

        # captured video request to server
        t3 = threading.Thread(target=self.send_frame_module, args=(frame_buffer, request_event))
        t3.start()

        # sound Player
        t4 = threading.Thread(target=self.sound_player)
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join

    def at_exit(self):
        self.servoTest3_instance.servo1_pwm.stop()
        self.servoTest3_instance.servo2_pwm.stop()
        self.servoTest3_instance.GPIO.cleanup()


if __name__ == "__main__":
    main = face_detector_cam()
    main.working()
