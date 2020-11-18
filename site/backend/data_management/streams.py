# pylint: disable=no-member
"""to stop pylint from complainign about cv2"""

import eventlet
import base64
import time
import cv2
import os

from dotenv import load_dotenv

import tempFileManger

from multiCam import MultiCam
from flask_socketio import emit
from commands import socketio, roboto

from flask import Blueprint, jsonify, request, render_template, Response
from flask_cors import CORS

bp = Blueprint('stream', __name__, url_prefix='/stream')

CORS(bp)

COUNT = 0
CAMERA = None


@socketio.on('connect')
def on_connect():
    print('[INFO] WebClient connected.')
    global COUNT

    COUNT = COUNT + 1

    if COUNT == 1:
        eventlet.sleep(1)
        socketio.start_background_task(startCams())


@socketio.on('disconnect')
def on_disconnect():
    print('[INFO] WebClient disconnected.')
    global COUNT
    global CAMERA

    COUNT = COUNT - 1
    roboto.stop()

    if COUNT == 0:
        del CAMERA
        CAMERA = None


@socketio.on('capture')
def capture():
    global CAMERA

    if (COUNT > 0):
        CAMERA.capture()


@socketio.on('refocus')
def refocus():
    global CAMERA

    if CAMERA.frontCam is not None:
        CAMERA.frontCam.refocus()


@socketio.on('swapImage')
def swapImage():
    global CAMERA

    CAMERA.flip = not CAMERA.flip


@socketio.on('startRecording')
def startRecording():
    global CAMERA
    tempFileManger.clearAll()
    CAMERA.startRecording()


@socketio.on('endRecording')
def endRecording():
    global CAMERA
    CAMERA.stopWriting()


def startCams():
    global COUNT
    global CAMERA

    REBOOT = False

    print(os.environ['CAM_RATIO'])
    print(COUNT)

    if (COUNT > 0 and CAMERA is None):
        CAMERA = MultiCam()

    eventlet.sleep()


def getCams():
    global CAMERA

    if CAMERA is None:
        startCams()

    while COUNT > 0 and not CAMERA.frontCam.reboot and not CAMERA.backCam.reboot:
        eventlet.sleep()
        # try:
        image = cv2.imencode('.jpg', CAMERA.generateFinalImage())

        if CAMERA.recording:
            CAMERA.writeVid(image)

        image = image[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
        # except:
        #    print('failed to create stream')

    try:
        if CAMERA and COUNT > 0:
            getCams()
    except:
        print("CAmera deleted unexpectedly")


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
