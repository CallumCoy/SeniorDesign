# pylint: disable=bare-except
"""to stop pylint from complainign about any excepts"""
import os
import time
import math
import eventlet

import Jetson.GPIO as GPIO
import Adafruit_PCA9685


def handler(_signalRecieved='', _frame=''):
    print("shutting motors off")

    safeNumber = 7
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(safeNumber, GPIO.OUT)
    except:
        print("board already declared")
    GPIO.output(safeNumber, GPIO.HIGH)


def stopRobot():
    print("halting robot")

    safeNumber = 7
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(safeNumber, GPIO.OUT)
    except:
        print("board already declared")
    GPIO.output(safeNumber, GPIO.HIGH)


class Robot:
    safeNumber = 7

    curID = 0

    motorEncoderPR = 570
    motorFrequency = 1600
    motorAddress = 0x41
    motorBusNum = 1

    # rightMotor
    rightMotorLoc = 0
    rightMotoReversed = True
    motor1DIR = 40
    motor1EncoderXPin = 13
    motor1EncoderYPin = 15

    # leftMotor
    leftMotorLoc = 15
    leftMotoReversed = False
    motor2DIR = 38
    motor2EncoderXPin = 11
    motor2EncoderYPin = 12

    servofrequency = 60
    servoAddress = 0x40
    servoBusNum = 1

    botServoPos = 15
    botServoMin = 91
    botServoRest = 293
    botServoMax = 490

    topServoPos = 0
    topServoMin = 100
    topServoRest = 360
    topServoMax = 490

    def __init__(self):

        self.setupBot()

        self.rightMotor = Motor(self.motor1EncoderXPin, self.motor1EncoderYPin, self.motorEncoderPR, self.motorAddress,
                                self.motorBusNum, self.rightMotorLoc, self.motor1DIR, self.rightMotoReversed, self.motorFrequency)
        self.leftMotor = Motor(self.motor2EncoderXPin, self.motor2EncoderYPin, self.motorEncoderPR, self.motorAddress,
                               self.motorBusNum, self.leftMotorLoc, self.motor2DIR, self.leftMotoReversed, self.motorFrequency)

        self.botServo = Servo(self.botServoMin, self.botServoRest, self.botServoMax,
                              self.botServoPos, self.servoAddress, self.servoBusNum, self.servofrequency)
        self.topServo = Servo(self.topServoMin, self.topServoRest, self.topServoMax,
                              self.topServoPos, self.servoAddress, self.servoBusNum, self.servofrequency)

        self.stop()

        GPIO.output(self. safeNumber, GPIO.LOW)

        self.topServo.goto(-0.5)
        self.botServo.rest()
        self.topServo.rest()

    def setupBot(self):

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.safeNumber, GPIO.OUT)

        GPIO.output(self. safeNumber, GPIO.HIGH)

        GPIO.setup(self.motor1DIR, GPIO.OUT)
        GPIO.setup(self.motor2DIR, GPIO.OUT)
        GPIO.setup(self.motor1EncoderXPin, GPIO.IN)
        GPIO.setup(self.motor1EncoderYPin, GPIO.IN)
        GPIO.setup(self.motor2EncoderXPin, GPIO.IN)
        GPIO.setup(self.motor2EncoderYPin, GPIO.IN)

        eventlet.sleep(0.1)

    def moveCamera(self, state, value):
        print(state)

        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.safeNumber, GPIO.OUT)
        except:
            print("board already declared")

        GPIO.output(self. safeNumber, GPIO.LOW)
        if state == 'x':
            self.botServo.goto(value)
        else:
            self.topServo.goto(value)

    def stop(self):
        self.rightMotor.stop()
        self.leftMotor.stop()

        GPIO.output(self.safeNumber, GPIO.HIGH)

    def releaseStop(self):
        GPIO.output(self.safeNumber, GPIO.LOW)

    def moveStraight(self, value):
        self.curID = (self.curID + 1) % 500
        taskID = self.curID

        if (value == 0):
            self.stopMotor("straight")
            return

        try:
            leftIncrement = 0.05 * (value / abs(value))
            rightIncrement = 0.05 * (value / abs(value))

            try:
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(self.safeNumber, GPIO.OUT)
            except:
                print("board already declared")

            GPIO.output(self. safeNumber, GPIO.LOW)

            while ((self.rightMotor.curSpeed > (value + 2 * rightIncrement) or self.rightMotor.curSpeed < (value - 2 * rightIncrement)) and
                    (self.leftMotor.curSpeed > (value + 2 * leftIncrement) or self.leftMotor.curSpeed < (value - 2 * leftIncrement)) and
                    taskID == self.curID):
                self.rightMotor.rotate(
                    self.rightMotor.curSpeed + rightIncrement)
                self.leftMotor.rotate(self.leftMotor.curSpeed + leftIncrement)

                eventlet.sleep(2/20)

            if (taskID == self.curID):
                self.rightMotor.rotate(value)
                self.leftMotor.rotate(value)

        except:
            print("failed to move")
            self.stopMotor()

    def rotate(self, value):
        self.curID = (self.curID + 1) % 500
        taskID = self.curID

        if (value == 0):
            self.stopMotor("turn")
            return

        try:
            rightValue = value * -1

            leftIncrement = 0.05 * (value / abs(value))
            rightIncrement = 0.05 * (rightValue / abs(rightValue))

            try:
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(self.safeNumber, GPIO.OUT)
            except:
                print("board already declared")

            GPIO.output(self. safeNumber, GPIO.LOW)

            while ((self.rightMotor.curSpeed > (rightValue + 2 * rightIncrement) or self.rightMotor.curSpeed < (rightValue - 2 * rightIncrement)) and
                    (self.leftMotor.curSpeed > (value + 2 * leftIncrement) or self.leftMotor.curSpeed < (value - 2 * leftIncrement)) and
                    taskID == self.curID):
                self.rightMotor.rotate(
                    self.rightMotor.curSpeed + rightIncrement)
                self.leftMotor.rotate(self.leftMotor.curSpeed + leftIncrement)

                eventlet.sleep(2/20)

            if (taskID == self.curID):
                self.leftMotor.rotate(value)
                self.rightMotor.rotate(rightValue)
        except:
            print("failed to move")
            self.stopMotor()

    def stopMotor(self, movementType="turn"):
        self.curID = (self.curID + 1) % 500
        taskID = self.curID

        try:
            if (self.leftMotor.curSpeed != 0):
                leftIncrement = 0.05 * (self.leftMotor.curSpeed /
                                        abs(self.leftMotor.curSpeed))
            else:
                leftIncrement = 0

            if (self.rightMotor.curSpeed != 0):
                rightIncrement = 0.05 * (self.rightMotor.curSpeed /
                                         abs(self.rightMotor.curSpeed))
            else:
                rightIncrement = 0

            while (abs(self.rightMotor.curSpeed) > rightIncrement and abs(self.leftMotor.curSpeed > leftIncrement) and
                    taskID == self.curID):

                self.rightMotor.rotate(
                    self.rightMotor.curSpeed - rightIncrement)
                self.leftMotor.rotate(self.leftMotor.curSpeed - leftIncrement)

                eventlet.sleep(1/20)

            if (taskID == self.curID):
                distance1 = self.rightMotor.stop()
                distance2 = self.leftMotor.stop()

                if movementType != "turn":
                    distance = (distance1 + distance2) / 2

                    print(math.pi * 2 *
                          (float(os.environ['WHEEL_RADIUS'])/12) * distance)

        except:
            print("DANGER failed to stop")
            try:
                handler(0, 0)
            except:
                print("DANGER DANGER DANGER DANGER everything failed")

    def ebrake(self, movementType="turn"):
        self.curID = (self.curID + 1) % 500
        print("Emergency Stop")
        try:
            distance1 = self.rightMotor.stop()
            distance2 = self.leftMotor.stop()
            if movementType != "turn":
                distance = (distance1 + distance2) / 2

                print(math.pi * 2 *
                      (float(os.environ['WHEEL_RADIUS'])/12) * distance)
        except:
            print("DANGER failed to stop")
            try:
                handler(0, 0)
            except:
                print("DANGER everything failed")


class Motor:

    maxSpeed = 4096
    curSpeed = 0

    encoderTotal = 0
    lastEncoder = ''

    def __init__(self, xEncoder, yEncoder, encoderRotation, address, busNum, motorPos, dirPin, reversedDir, frequency):

        GPIO.add_event_detect(xEncoder, GPIO.RISING,
                              callback=self.xCallback)
        GPIO.add_event_detect(yEncoder, GPIO.RISING,
                              callback=self.yCallback)

        self.encoderRot = encoderRotation

        self.pwmController = Adafruit_PCA9685.PCA9685(
            address=address, busnum=busNum)
        self.pwmController.set_pwm_freq(frequency)

        self.motorPos = motorPos
        self.dirPin = dirPin
        self.reversed = reversedDir

    def __delete__(self, instance):
        if self.reversed:
            GPIO.output(self.dirPin, GPIO.LOW)
        else:
            GPIO.output(self.dirPin, GPIO.HIGH)
        self.stop()

    def xCallback(self, _pin):
        if self.curSpeed > 0:
            if self.lastEncoder == 'x':
                self.encoderTotal += 2
            else:
                self.encoderTotal += 1
        else:
            if self.lastEncoder == 'x':
                self.encoderTotal -= 2
            else:
                self.encoderTotal -= 1

        self.lastEncoder = 'x'

    def yCallback(self, _pin):
        if self.curSpeed > 0:
            if self.lastEncoder == 'y':
                self.encoderTotal += 2
            else:
                self.encoderTotal += 1
        else:
            if self.lastEncoder == 'y':
                self.encoderTotal -= 2
            else:
                self.encoderTotal -= 1

        self.lastEncoder = 'y'

    def rotate(self, percent):

        if (self.curSpeed - percent == 0):
            return
        elif(abs(percent) > 1):
            return
        elif (abs(self.curSpeed - percent) > 0.5):
            print("DANGER speeding up by more than 5% {} - {} = {}".format(
                self.curSpeed, percent, (self.curSpeed - percent)))
            return
        elif round(percent, 2) == 0.00:
            self.curSpeed = self.curSpeed - percent
            return

        self.curSpeed = percent

        if self.reversed:
            percent = percent * -1
        if percent > 0:
            GPIO.output(self.dirPin, GPIO.HIGH)
        elif percent < 0:
            GPIO.output(self.dirPin, GPIO.LOW)
        else:
            return

        power = abs(percent)
        if power != 1 and power != 0:
            power = 1 - power

        self.pwmController.set_pwm(
            self.motorPos, round(self.maxSpeed * power), 0)

    def stop(self):
        self.curSpeed = 0
        self.pwmController.set_pwm(self.motorPos, 0, 0)
        rotations = self.encoderTotal / self.encoderRot

        self.encoderTotal = 0
        self.lastEncoder = ''

        return rotations


class Servo:
    servoStop = False
    servoHold = False

    def __init__(self, servoMin, servoRest, servoMax, servoNum, address, busnum, frequency):
        self.servoMin = servoMin
        self.servoMax = servoMax
        self.servoRest = servoRest
        self.servoPos = servoRest
        self.servoNum = servoNum

        self.pwmController = Adafruit_PCA9685.PCA9685(
            address=address, busnum=busnum)
        self.pwmController.set_pwm_freq(frequency)

    def __delete__(self, instance):
        self.stop()
        self.rest()

    def goto(self, percent):
        if not self.servoHold:
            self.servoStop = True
            deviation = 0
            print(percent)
            if percent < 0:
                deviation = (self.servoRest - self.servoMin) * percent
            elif percent > 0:
                deviation = (self.servoMax - self.servoRest) * percent

            self.stop()

            self.travel(self.servoRest - deviation)

    def travel(self, target):
        if (self.servoPos - target) == 0:
            return
        interval = (self.servoPos - target) / abs(self.servoPos - target) * -1

        while not self.servoStop and not self.servoHold and self.servoPos != round(target):

            self.servoPos += interval
            self.pwmController.set_pwm(
                self.servoNum, 0, round(self.servoPos))

            if (self.servoPos % 5 == 0):
                eventlet.sleep()

    def rest(self):
        self.pwmController.set_pwm(self.servoNum, 0, self.servoRest)

    def stop(self):
        print("stopping servo " + str(self.servoNum))
        self.servoStop = True
        eventlet.sleep(0.005)
        self.servoStop = False

    def servoHoldToggle(self):
        self.servoHold = not self.servoHold
