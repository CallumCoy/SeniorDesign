# pylint: disable=no-member
"""to stop pylint from complainign about cv2"""
# pylint: disable=global-statement
"""to stop pylint from complainign about any excepts"""


import time
from dotenv import load_dotenv
from flask_socketio import emit
from flask import Blueprint, jsonify, request, render_template, Response
from flask_cors import CORS
import numpy as np
import eventlet
import base64
import cv2
import os
import tempFileManger
from multiCam import MultiCam
from commands import socketio, roboto
bp = Blueprint('stream', __name__, url_prefix='/stream')

CORS(bp)

COUNT = 0
CAMERA = None
LASTPING = time.time()
CHECKRUNNING = False
CAPTURE = False


@socketio.on('connect')
def on_connect():
    global COUNT
    print('[INFO] WebClient connected.')
    global LASTPING

    COUNT = COUNT + 1
    LASTPING = time.time()


@socketio.on('disconnect')
def on_disconnect():
    print('[INFO] WebClient disconnected.')
    global COUNT

    COUNT = COUNT - 1
    print(COUNT)
    roboto.stopMotor("turn")


@bp.route('/check', methods=(['POST']))
def check():
    global LASTPING
    global CHECKRUNNING

    LASTPING = time.time()

    if not CHECKRUNNING:
        roboto.stopMotor("turn")
        checkComp()

    return jsonify({})


def checkComp():
    global LASTPING
    global CHECKRUNNING

    CHECKRUNNING = True
    while time.time() - LASTPING <= 2.2:
        eventlet.sleep(1)

    print("failed to get ping within alloted time")

    CHECKRUNNING = False
    roboto.ebrake()


@socketio.on('capture')
def capture():
    global CAPTURE

    CAPTURE = True


@socketio.on('refocus')
def refocus():
    global CAMERA

    if CAMERA.backCam is not None:
        CAMERA.backCam.refocus()


@socketio.on('swapImage')
def swapImage():
    global CAMERA
    if CAMERA is not None:
        CAMERA.flip = not CAMERA.flip


@socketio.on('run')
def startRecording(bearing, lat, longi, record):
    global CAMERA
    tempFileManger.clearAll()

    if CAMERA is not None and not CAMERA.recording and record:
        CAMERA.startRecording()

    if CAMERA is not None and not CAMERA.recording:
        CAMERA.tagCount = 0
        CAMERA.allowCapture = True
        CAMERA.recordTime = time.time()
        roboto.lat = lat
        roboto.long = longi
        roboto.bearing = bearing


@socketio.on('endRecording')
def endRecording():
    global CAMERA

    if CAMERA is not None and CAMERA.recording:
        CAMERA.stopRecording()

    CAMERA.allowCapture = False


def startCams():
    global COUNT
    global CAMERA

    REBOOT = False

    if (COUNT > 0 and CAMERA is None):
        CAMERA = MultiCam()

    eventlet.sleep(1.5)


def getCams():
    global CAMERA
    global CAPTURE

    if CAMERA is None:
        startCams()

    lastSave = time.time() - 1

    while CAMERA is not None and COUNT > 0:
        # try:

        image = CAMERA.generateFinalImage()

        if CAMERA.recording and time.time() - lastSave > 1/int(os.environ.get("FPS")):
            socketio.start_background_task(
                CAMERA.writeVid, image)
            lastSave = time.time()

        if CAPTURE and CAMERA.allowCapture:
            CAPTURE = False
            (tagNum, lat, longi, dist, timerCapture) = CAMERA.capture(image)
            socketio.emit(socketio.emit("addTag",
                                        {"Position": tagNum,
                                         "Lat": lat,
                                         "Longi": longi,
                                         "Distance": dist,
                                         "VideoTime": timerCapture}))
        elif CAPTURE:
            CAPTURE = False

        image = cv2.imencode('.jpg', image)[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
        eventlet.sleep()

        # except:
        #    print('failed to create stream')

    del CAMERA
    CAMERA = None


@bp.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


@bp.route('/video_feed')
def showCams():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(getCams(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def toJPG(frame):
    _ret, jpeg = cv2.imencode('.jpg', frame)
    return jpeg


def encodeFrame(frame):
    return base64.b64encode(frame.tobytes()).decode('utf-8')
