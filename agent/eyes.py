import cv2


class Eyes(object):

    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def release(self):
        self.cap.release()

