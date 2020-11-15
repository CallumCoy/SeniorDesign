# pylint: disable=no-member
"""to stop pylint from complainign about cv2"""

import base64
import time
import cv2
import os

from dotenv import load_dotenv

import tempFileManger

from video import Video
from flask_socketio import emit
from robotSetup import stopRobot
from commands import socketio


COUNT = 0
TAGCOUNT = 0
REBOOT = False
VIDEO = []


@socketio.on('connect')
def on_connect():
    print('[INFO] WebClient connected.')
    global COUNT

    COUNT = COUNT + 1

    if COUNT == 1:
        time.sleep(1)
        socketio.start_background_task(emitCams)


@socketio.on('disconnect')
def on_disconnect():
    print('[INFO] WebClient disconnected.')
    global COUNT
    COUNT = COUNT - 1
    stopRobot()


@socketio.on('capture')
def capture(cam):
    global VIDEO
    global TAGCOUNT

    if (COUNT > 0 and 0 not in VIDEO):
        try:
            sample1 = VIDEO[0].genCam()
            yDim = sample1.shape[0]
            xDim = sample1.shape[1]
            try:
                sample2 = VIDEO[1].genCam()
                yOffset = yDim - sample2.shape[0]
                xOffset = xDim - sample2.shape[1]
            except:
                print("camera 2 missing")
        except:
            print("camera 1 missing")

        img = createImage(xDim, yDim, xOffset, yOffset)
        cv2.imwrite('temp/tag{}.jpg'.format(TAGCOUNT), img)

        timerCapture = VIDEO[cam].getTime()

        # location Request
        # send frontend details

        socketio.emit("addTag",
                      {"Position": TAGCOUNT,
                       "Lat": 0,
                       "Longi": 0,
                       "VideoTime": timerCapture})

        TAGCOUNT = TAGCOUNT + 1


@socketio.on('refocus')
def refocus():
    global VIDEO

    for item in VIDEO:
        item.refocus()


@socketio.on('startRecording')
def startRecording():
    global VIDEO
    global TAGCOUNT
    TAGCOUNT = 0
    tempFileManger.clearAll()
    VIDEO[0].startWriting()


@socketio.on('endRecording')
def endRecording():
    global VIDEO
    VIDEO[0].stopWriting()


def emitCams():
    global COUNT
    global VIDEO

    REBOOT = False

    if ('FPS' in os.environ):
        os.environ.pop('FPS')

    load_dotenv("../.env")
    print(os.environ['CAM_RATIO'])
    print(COUNT)

    if (COUNT > 0 and 0 not in VIDEO):
        VIDEO.insert(0, Video(0, int(os.environ.get("FPS")), 0, True))

    if (COUNT > 0 and 1 not in VIDEO):
        VIDEO.insert(1, Video(1, int(os.environ.get("FPS")), 0, True))

    try:
        sample1 = VIDEO[0].genCam()
        yDim = sample1.shape[0]
        xDim = sample1.shape[1]
        try:
            sample2 = VIDEO[1].genCam()
            yOffset = yDim - sample2.shape[0]
            xOffset = xDim - sample2.shape[1]
        except:
            print("camera 2 missing")
    except:
        print("camera 1 missing")

    try:
        while COUNT > 0 and not VIDEO[0].reboot and not REBOOT:
            img = toJPG(encodeFrame(createImage(xDim, yDim, xOffset, yOffset)))
            socketio.emit("streamOut", img)

    except:
        print('failed to create camera')

    if 0 in VIDEO:
        del VIDEO[0]
    VIDEO = []

    if COUNT < 0:
        emitCams()


def createImage(xDim, yDim, xOffset, yOffset):

    global VIDEO

    if 1 not in VIDEO:
        return VIDEO[0].genCam()

    mainImage = VIDEO[0].genCam()
    secondaryImage = VIDEO[1].genCam()

    mainImage[yOffset:yOffset+yDim, xOffset:xOffset+xDim] = secondaryImage
    return mainImage


def toJPG(frame):
    _ret, jpeg = cv2.imencode('.jpg', frame)
    return jpeg


def encodeFrame(frame):
    return base64.b64encode(frame.tobytes()).decode('utf-8')


def rebootStream():
    global REBOOT
    REBOOT = True
