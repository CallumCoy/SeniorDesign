# pylint: disable=no-member
"""to stop pylint from complainign about cv2"""
# pylint: disable=bare-except
"""to stop pylint from complainign about any excepts"""




import eventlet
import time
import cv2
import os
from dotenv import load_dotenv
from video import Video
class MultiCam(object):

    codec = 'avc1'
    videoType = 'mp4'

    tagCount = 0

    recording = False

    flip = False

    frontCamIndex = 1
    frontCamJetson = True
    frontCamFlip = 0
    frontCamAllowFocus = False

    backCamIndex = 0
    backCamJetson = True
    backCamFlip = 0
    backCamAllowFocus = False

    camFPS = 10

    yOffset = 0
    xOffset = 0

    yDim = 0

    def __init__(self):
        failCount = 0

        if ('FPS' in os.environ):
            os.environ.pop('FPS')

        load_dotenv("/home/sewerbot/repo/SeniorDesign/site/backend/.env")

        print(os.environ.get("FPS"))

        try:
            self.frontCam = Video(self.frontCamIndex, int(os.environ.get(
                "FPS")), self.frontCamFlip, self.frontCamJetson, self.frontCamAllowFocus)
        except:
            print("failed to insert Camera 1")
            failCount += 1

        try:
            self.backCam = Video(self.backCamIndex, int(os.environ.get(
                "FPS")), self.backCamFlip, self.backCamJetson, self.backCamAllowFocus)
        except:
            print("failed to insert Camera 2")
            failCount += 1

        self.generatOverlayValues()

    def generatOverlayValues(self):

        if ('CAM_RATIO' in os.environ):
            os.environ.pop('CAM_RATIO')

        load_dotenv("/home/sewerbot/repo/SeniorDesign/site/backend/.env")

        print('CAMRATIO = ' + os.environ['CAM_RATIO'])

        try:
            sample1 = self.frontCam.genCam()
            self.yOffset = int(
                sample1.shape[0] * (1 - float(os.environ['CAM_RATIO'])))
            self.xOffset = int(
                sample1.shape[1] * (1 - float(os.environ['CAM_RATIO'])))
        except:
            print("camera 1 missing")

        try:
            sample2 = self.backCam.genCam()
            self.yDim = int(sample2.shape[0]
                            * float(os.environ['CAM_RATIO']))
            self.xDim = int(sample2.shape[1]
                            * float(os.environ['CAM_RATIO']))
        except:
            print("camera 2 missing")
            try:
                self.yDim = int(sample1.shape[0]
                                * float(os.environ['CAM_RATIO']))
                self.xDim = int(sample1.shape[1]
                                * float(os.environ['CAM_RATIO']))
            except:
                self.yDim = 0
                self.xDim = 0
                print("catching dimensions")

        self.dim = (self.xDim, self.yDim)

    def generateFinalImage(self):
        if self.backCam is None:
            return self.frontCam.genCam()

        elif self.frontCam is None:
            return self.backCam.genCam()

        if self.flip:
            mainImage = self.frontCam.genCam()
            secondaryImage = self.backCam.genCam()
        else:
            mainImage = self.backCam.genCam()
            secondaryImage = self.frontCam.genCam()

        if secondaryImage is None:
            return mainImage

        elif mainImage is None:
            return secondaryImage

        smallFrame = cv2.resize(secondaryImage, self.dim)

        mainImage[self.yOffset: self.yOffset + self.yDim,
                  self.xOffset: self.xOffset + self.xDim] = smallFrame

        return mainImage

    def capture(self):
        img = self.generateFinalImage()
        cv2.imwrite('temp/tag{}.jpg'.format(self.tagCount), img)

        timerCapture = time.time() - self.recordTime

        # location Request
        # send frontend details

        return ("addTag",
                {"Position": self.tagCount,
                 "Lat": 0,
                 "Longi": 0,
                 "VideoTime": timerCapture})

        self.tagCount += 1

    def startRecording(self):
        self.tagCount = 0
        self.recordTime = time.time()

        cv2.imwrite('temp/imageFront.jpg', self.generateFinalImage())
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        self.record = cv2.VideoWriter('temp/outputtedVideo.{}'.format(self.videoType),
                                      fourcc,
                                      int(os.environ.get("FPS")),
                                      (self.xDim, self.yDim))
        self.recording = True

    def writeVid(self, frame):
        self.record.write(frame)

    def stopRecording(self):
        self.recording = False
        self.record.release()
