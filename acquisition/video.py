# Better samples/python2/opt_flow.py
# for Raspberry Pi

## reference
# - http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# - http://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python
# - http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

import time
import cv2


class VideoInput:
    def capture(self):
        raise NotImplementedError('implement capture function')

    def destroy(self):
        pass


class PiCameraLiveInput(VideoInput):
    def __init__(self) -> None:
        from picamera2 import Picamera2
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(main={'format': 'RGB888'})
        picam2.configure(config)
        picam2.start()
        time.sleep(1)  # wait for camera to initialize
        self.camera = picam2

    def capture(self):
        array = self.camera.capture_array('main')
        return array

    def destroy(self):
        self.camera.stop()
        return super().destroy()


class RecordedVideoInput(VideoInput):
    def __init__(self, video_url) -> None:
        super().__init__()
        self._video_url = video_url


class LiveVideoInput(VideoInput):
    def __init__(self) -> None:
        super().__init__()
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise Exception('Camera could not initialize')
        self.camera = camera
    
    def capture(self):
        rval, frame = self.camera.read()
        return frame


def get_camera(video_url=None) -> VideoInput:
    try:
        return PiCameraLiveInput()
    except Exception:
        if video_url:
            return RecordedVideoInput(video_url)
        else:
            return LiveVideoInput()
