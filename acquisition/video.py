# Better samples/python2/opt_flow.py
# for Raspberry Pi

## reference
# - http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# - http://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python
# - http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

import time
import cv2

from preprocessing.video_slicing import MP4VideoSlicer
from preprocessing.image_operations import crop_cv_image_centered, resize_cv_image_to_maxwidth


class BaseVideoInput:
    def capture(self) -> cv2.typing.MatLike:
        raise NotImplementedError('implement capture function')

    def destroy(self):
        pass


class PiCameraLiveInput(BaseVideoInput):
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


class RecordedVideoInput(BaseVideoInput):
    def __init__(self, video_url) -> None:
        super().__init__()
        self._video_url = video_url
        self.videoslicer = MP4VideoSlicer(video_url)
        self.is_started = False
        self.last_timestamp = None

    def capture(self):
        new_timestamp = time.time()
        if self.last_timestamp is None:
            self.last_timestamp = new_timestamp
        else:
            difference = new_timestamp - self.last_timestamp
            print(f'{(1/difference):02f}', end='\r')
            self.last_timestamp = new_timestamp
            self.videoslicer.next_step_seconds = difference
        try:
            rval, frame = next(self.videoslicer)
            return resize_cv_image_to_maxwidth(crop_cv_image_centered(frame, 1), max_width=400)
        except Exception as e:
            self.videoslicer.cleanup()
            raise e

    def destroy(self):
        self.videoslicer.cleanup()
        return super().destroy()


class DefaultCameraVideoInput(BaseVideoInput):
    def __init__(self) -> None:
        super().__init__()
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise Exception('Camera could not initialize')
        self.camera = camera
    
    def capture(self):
        rval, frame = self.camera.read()
        return frame


def get_camera(video_url=None) -> BaseVideoInput:
    try:
        return PiCameraLiveInput()
    except Exception:
        if video_url:
            return RecordedVideoInput(video_url)
        else:
            return DefaultCameraVideoInput()
