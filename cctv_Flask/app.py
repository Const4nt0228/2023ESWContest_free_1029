import cv2
import numpy as np
from flask import Flask, request, Response  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import

import paho.mqtt.client as mqtt
from time import sleep

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록
frame_queue = []
frame_queue_dict = {}

frame_queue_dict['client1'] = []


def display_frames():
    while True:
        if len(frame_queue) == 0:
            continue
        frame = frame_queue[-1]
        cv2.imshow(f'Server Monitor', frame)  # 윈도우 창에 프레임 띄우기
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def display_frames_dict():
    while True:
        # print(frame_queue_dict)
        if len(frame_queue_dict["client1"]) == 0:
            # print('len continue')
            continue
        # print(frame)
        frame = frame_queue_dict["client1"][-1]
        cv2.imshow(f'Server Monitor : [{"client1"}]', frame)  # 윈도우 창에 프레임 띄우기
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


@api.route('/cctv/cctv_move/')
class cctvMove(Resource):
    def put(self):
        payload = request.get_json()
        print(payload['move'])

        mqttc = mqtt.Client(f"django_pub_{payload['cctv']}")  # puclisher 이름
        mqttc.connect("***********", 1883)
        sleep(0.1)

        mqttc.publish("move", payload['move'])  # topic, message

        return {"success": "dd"}


@app.route('/upload_frame/<client_id>', methods=['POST'])
def upload_frame_dict(client_id):
    frame_data = request.data
    frame_array = np.frombuffer(frame_data, dtype=np.uint8)
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

    if client_id not in frame_queue_dict:
        frame_queue_dict[client_id] = []

    frame_queue_dict[client_id].append(frame)
    # print(frame_queue_dict[client_id])
    if len(frame_queue_dict[client_id]) > 10:  # 프레임 큐 크기 제한을 설정할 수 있습니다.
        frame_queue_dict[client_id].pop(0)

    # 애는 팝 기능이 없어서,

    return 'Frame uploaded successfully'


def generate_frames(client_id):
    while True:
        if client_id in frame_queue_dict and len(frame_queue_dict[client_id]) > 0:
            frame = frame_queue_dict[client_id][-1]
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed/<client_id>')
def video_feed(client_id):
    return Response(generate_frames(client_id), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    frame_data = request.data
    frame_array = np.frombuffer(frame_data, dtype=np.uint8)
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

    frame_queue.append(frame)
    if len(frame_queue) > 10:  # 프레임 큐 크기 제한을 설정할 수 있습니다.
        frame_queue.pop(0)

    return 'Frame uploaded successfully'


if __name__ == "__main__":
    import threading
    #
    # threading.Thread(target=display_frames_dict).start()

    app.run(debug=True, host='0.0.0.0', port=8080)
