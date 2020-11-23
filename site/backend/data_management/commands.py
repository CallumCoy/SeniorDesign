from robotSetup import Robot

from flask_socketio import SocketIO


socketio = SocketIO(cors_allowed_origins="*")


roboto = Robot()


@socketio.on('binary')
def binary(_state):
    print("binary pressed")


@socketio.on('stop')
def stop():
    socketio.start_background_task(roboto.stop)

    socketio.start_background_task(roboto.botServo.rest)
    socketio.start_background_task(roboto.topServo.rest)


@socketio.on('stopCam')
def stopCam(target):
    print("stop Cam")
    if target is None:
        socketio.start_background_task(roboto.botServo.stop)
        socketio.start_background_task(roboto.topServo.stop)
    elif 'x' in target:
        socketio.start_background_task(roboto.botServo.stop)
    else:
        socketio.start_background_task(roboto.topServo.stop)


@socketio.on('speed')
def speed(_state):
    print("speed sent")


@socketio.on('movement')
def movement(state, value):
    if state == 'straight':
        socketio.start_background_task(roboto.moveStraight(value))
    else:
        socketio.start_background_task(roboto.rotate(value))


@socketio.on('stopMotors')
def stopMotor(target):
    if(target == None):
        socketio.start_background_task(roboto.stopMotor(movementType='turn'))
    else:
        socketio.start_background_task(roboto.stopMotor(movementType=target))


@ socketio.on('camera')
def camera(state, value):
    socketio.start_background_task(roboto.moveCamera(state, value))


@ socketio.on('camHolt')
def camHolt():
    socketio.start_background_task(roboto.botServo.servoHoldToggle())
    socketio.start_background_task(roboto.topServo.servoHoldToggle())
