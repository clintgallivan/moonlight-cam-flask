# from flask import Flask, render_template, Response
# import cv2
# # yep

# app = Flask(__name__)
# # camera = cv2.VideoCapture(0)
# # camera = cv2.VideoCapture(
# # "rtsp://username:password@192.168.1.16:8554/profile0")
# camera = cv2.VideoCapture(
#     "rtsp://username:password@174.65.33.32:8554/profile0")


# # def make_480p():
# #     camera.set(3, 640)
# #     camera.set(4, 480)


# def generate_frames():
#     while True:

#       # read the camera frame
#         success, frame = camera.read()
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#         yield(b'--frame\r\n'
#               b'Content-Type: image\jpeg\r\n\r\n' + frame + b'\r\n')


# @app.route('/')
# def index():
#     return render_template('index2.html')


# @app.route('/video')
# def video():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# from flask import Flask, render_template, Response
# import cv2
# import threading
# import time
# import queue


# # bufferless VideoCapture

# app = Flask(__name__)


# class VideoCapture:

#     def __init__(self, name):
#         self.cap = cv2.VideoCapture(name)
#         self.q = queue.Queue()
#         t = threading.Thread(target=self._reader)
#         t.daemon = True
#         t.start()

#     # read frames as soon as they are available, keeping only most recent one
#     def _reader(self):
#         while True:
#             ret, frame = self.cap.read()
#             if not ret:
#                 break
#             if not self.q.empty():
#                 try:
#                     self.q.get_nowait()   # discard previous (unprocessed) frame
#                 except queue.Empty:
#                     pass
#             self.q.put(frame)

#     def read(self):
#         return self.q.get()


# cap = VideoCapture("rtsp://username:password@174.65.33.32:8554/profile0")


# def generate_frames():
#     while True:
#         time.sleep(.5)
#         frame = cap.read()
#         print(frame)

#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         yield(b'--frame\r\n'
#               b'Content-Type: image\jpeg\r\n\r\n' + frame + b'\r\n')


# @app.route('/')
# def index():
#     return render_template('index2.html')


# @app.route('/video')
# def video():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


from cv2 import CAP_PROP_FPS, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH, rotate
from flask import Flask, render_template, Response
import cv2
import threading
import time
import queue
import numpy as np


# bufferless VideoCapture

app = Flask(__name__)


class VideoCapture:

    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        self.frame_width = self.cap.get(CAP_PROP_FRAME_WIDTH)
        self.frame_height = self.cap.get(CAP_PROP_FRAME_HEIGHT)
        # print(self.frame_height)
        # print(self.frame_width)

        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            rotated = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            cropped_img = rotated[100:500, 0:885]
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(cropped_img)

    def read(self):
        return self.q.get()


cap = VideoCapture("rtsp://username:password@174.65.33.32:8554/profile0")


def generate_frames():
    while True:
        time.sleep(.5)
        frame = cap.read()
        # print(cap.__dict__)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield(b'--frame\r\n'
              b'Content-Type: image\jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
