import cv2

video = cv2.VideoCapture('rtsp://192.168.1.16:8554/profile0')

while True:
    _, frame = video.read()
    cv2.imshow("RTSP", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break


video.release()
cv2.destroyAllWindows()
