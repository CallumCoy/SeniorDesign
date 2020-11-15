# pylint: disable=no-member
"""to stop pylint from complainign about cv2"""

import time
import cv2
import os


VIDEOTYPE = 'mp4'
CODEC = 'avc1'


class Video(object):
    """object that contains all command each camera may need"""
    jetson = False
    max_index = 10
    max_value = 0.0
    last_value = 0.0
    skip_frame = 2
    dec_count = 0
    focuser = False
    focal_distance = 10
    focus_finished = False

    fps = None
    reboot = False
    cameraTarg = None
    captureDev = None
    recording = False
    frameWidth = 1280
    frameHeight = 720
    recordTime = time.time()

    def __init__(self, target, fps, flip, jetson):
        print(jetson)
        if jetson:
            # Jetson setup
            #(capture_width, capture_height, display_width, display_height, framerate, flip_method)
            self.captureDev = cv2.VideoCapture(jetsonCamSetup(
                capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=fps, flip_method=flip), cv2.CAP_GSTREAMER)
            print(jetsonCamSetup(capture_width=1280, capture_height=720,
                                 display_width=1280, display_height=720, framerate=fps, flip_method=flip))
        else:
            self.captureDev = cv2.VideoCapture(target)

        self.fps = fps
        self.cameraTarg = target
        self.frameWidth = int(self.captureDev.get(3))  # 1280
        self.frameHeight = int(self.captureDev.get(4))  # 720
        self.jetson = jetson

    def __delete__(self, instance):
        self.record.release()
        self.captureDev.release()

    def genCam(self):
        _ret, frame = self.captureDev.read()

        if(frame is None):
            print('calling camera reboot')
            self.reboot = True
            return

        if self.recording:
            self.writeVid(frame)

        if not self.jetson:
            time.sleep(1/self.fps)
        else:
            self.focus(frame)

        return frame

    def startWriting(self):
        global CODEC
        global VIDEOTYPE

        cv2.imwrite('temp/imageFront.jpg', self.getFrame())
        fourcc = cv2.VideoWriter_fourcc(*CODEC)
        self.record = cv2.VideoWriter('temp/outputtedVideo.{}'.format(VIDEOTYPE),
                                      fourcc,
                                      self.fps,
                                      (self.frameWidth, self.frameHeight))
        self.recording = True

    def writeVid(self, frame):
        self.record.write(frame)

    def stopWriting(self):
        self.recording = False
        self.record.release()

    def captureImage(self):
        return self.getFrame()

    def getTime(self):
        return time.time() - self.recordTime

    def focus(self, img):
        if self.dec_count < 6 and self.focal_distance < 1000:
            # Adjust focus
            self.focusing(self.focal_distance)
            # Take image and calculate image clarity
            val = self.laplacian(img)
            # Find the maximum image clarity
            if val > self.max_value:
                self.max_index = self.focal_distance
                self.max_value = val

            # If the image clarity starts to decrease
            if val < self.last_value:
                self.dec_count += 1
            else:
                self.dec_count = 0
            # Image clarity is reduced by six consecutive frames
            if self.dec_count < 6:
                self.last_value = val
                # Increase the focal distance
                self.focal_distance += 10

        elif not self.focus_finished:
            # Adjust focus to the best
            self.focusing(self.max_index)
            self.focus_finished = True

    def refocus(self):
        self.focus_finished = False

    def focusing(self, val):
        value = (val << 4) & 0x3ff0
        data1 = (value >> 8) & 0x3f
        data2 = value & 0xf0
        os.system("i2cset -y 6 0x0c %d %d" % (data1, data2))
        #self.focuser.set(Focuser.OPT_FOCUS, val)

    def sobel(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_sobel = cv2.Sobel(img_gray, cv2.CV_16U, 1, 1)
        return cv2.mean(img_sobel)[0]

    def laplacian(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_sobel = cv2.Laplacian(img_gray, cv2.CV_16U)
        return cv2.mean(img_sobel)[0]


def jetsonCamSetup(capture_width, capture_height, display_width, display_height, framerate, flip_method):
    return ('nvarguscamerasrc ! '
            'video/x-raw(memory:NVMM), '
            'width=(int)%d, height=(int)%d, '
            'format=(string)NV12, framerate=(fraction)%d/1 ! '
            'nvvidconv flip-method=%d ! '
            'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
            'videoconvert ! '
            'video/x-raw, format=(string)BGR ! appsink' % (capture_width, capture_height, framerate, flip_method, display_width, display_height))
