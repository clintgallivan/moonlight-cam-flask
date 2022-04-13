from flask import Flask, render_template, Response
import cv2
# yep

app = Flask(__name__)
# camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture(
# "rtsp://username:password@192.168.1.16:8554/profile0")
camera = cv2.VideoCapture(
    "rtsp://username:password@174.65.33.32:8554/profile0")


def generate_frames():
    while True:

      # read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
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


if __name__ == "__main__":
    app.run(debug=True)
