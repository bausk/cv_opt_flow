# Better samples/python2/opt_flow.py
# for Raspberry Pi

## reference
# - http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# - http://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python
# - http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

import time
import cv2
from picamera2 import Picamera2
import numpy as np
from OpticalFlowShowcase import *

usage_text = '''
Hit followings to switch to:
1 - Dense optical flow by HSV color image (default);
2 - Dense optical flow by lines;
3 - Dense optical flow by warped image;
4 - Lucas-Kanade method.

Hit 's' to save image.

Hit 'f' to flip image horizontally.

Hit ESC to exit.
'''

def main():
    ## private routines
    def change(key, prevFrame):
        message, type = {
            ord('1'): ('==> Dense_by_hsv', 'dense_hsv'),
            ord('2'): ('==> Dense_by_lines', 'dense_lines'),
            ord('3'): ('==> Dense_by_warp', 'dense_warp'),
            ord('4'): ('==> Lucas-Kanade', 'lucas_kanade')
        }.get(key, ('==> Dense_by_hsv', 'dense_hsv'))
        print(message)
        of = CreateOpticalFlow(type)
        of.set1stFrame(prevFrame)
        return of
    
    ## main starts here
    flipImage = True
    of = None
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "RGB888"})
    picam2.configure(config)
    picam2.start()
    time.sleep(1)  # wait for camera to initialize
            
    cv2.namedWindow("preview")

    ## main work
    for _ in range(1000):  # Adjust the range according to your needs
        # capture frame
        array = picam2.capture_array("main")
        # frame = np.array(array.get_data(), dtype=np.uint8).reshape((array.height, array.width, 3))
        frame = array

        if of is None:
            of = change(ord('1'), frame)
            continue

        ### flip
        if flipImage:
            frame = cv2.flip(frame, 1)

        ### do it
        img = of.apply(frame)
        cv2.imshow("preview", img)

        ### key operation
        key = cv2.waitKey(1)
        if key == 27:         # exit on ESC
            print('Closing...')
            break
        elif key == ord('s'):   # save
            cv2.imwrite('img_raw.png', frame)
            cv2.imwrite('img_w_flow.png', img)
            print("Saved raw frame as 'img_raw.png' and displayed as 'img_w_flow.png'")
        elif key == ord('f'):   # save
            flipImage = not flipImage
            print("Flip image: " + {True: "ON", False: "OFF"}.get(flipImage))
        elif ord('1') <= key <= ord('4'):
            of = change(key, frame)

    ## finish
    picam2.stop()
    cv2.destroyWindow("preview")


if __name__ == '__main__':
    print(usage_text)
    main()
