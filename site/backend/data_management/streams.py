# pylint: disable=no-member
"""to stop pylint from complainign about cv2"""
# pylint: disable=global-statement
"""to stop pylint from complainign about any excepts"""


import time
from dotenv import load_dotenv
from flask_socketio import emit
from flask import Blueprint, jsonify, request, render_template, Response
from flask_cors import CORS
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


@socketio.on('connect')
def on_connect():
    print('[INFO] WebClient connected.')
    global COUNT
    global LASTPING

    COUNT = COUNT + 1
    LASTPING = time.time()

    if COUNT == 1:
        checkComp()
        eventlet.sleep(1)
        socketio.start_background_task(startCams())


@socketio.on('disconnect')
def on_disconnect():
    print('[INFO] WebClient disconnected.')
    global COUNT
    global CAMERA

    COUNT = COUNT - 1
    roboto.stopMotor("turn")


@bp.route('/check', methods=(['POST']))
def check():
    global LASTPING

    LASTPING = time.time()

    if LASTPING - time.time() > 1:
        checkComp()

    return jsonify({})


def checkComp():
    global LASTPING
    while time.time() - LASTPING <= 1:
        eventlet.sleep(0.9)
    print("failed to get ping within alloted time")
    roboto.stopMotor("turn")


@socketio.on('capture')
def capture():
    global CAMERA

    if (COUNT > 0):
        CAMERA.capture()


@socketio.on('refocus')
def refocus():
    global CAMERA

    if CAMERA.backCam is not None:
        CAMERA.backCam.refocus()


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

    print(COUNT)

    if (COUNT > 0 and CAMERA is None):
        CAMERA = MultiCam()

    eventlet.sleep()


def getCams():
    global CAMERA
    print("test")

    if CAMERA is None:
        startCams()

    while COUNT > 0:
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
        print("Camera deleted unexpectedly")


@bp.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


@bp.route('/video_feed')
def showCams():
    """Video streaming route. Put this in the src attribute of an img tag."""
    print('test1')
    return Response(getCams(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def toJPG(frame):
    _ret, jpeg = cv2.imencode('.jpg', frame)
    return jpeg


def encodeFrame(frame):
    return base64.b64encode(frame.tobytes()).decode('utf-8')
