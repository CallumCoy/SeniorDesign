import os
import json

from flask import Blueprint, jsonify, request
from flask_cors import CORS

from db import getDb
from get import getVideo
from tempFileManger import moveFiles

bp = Blueprint('save', __name__, url_prefix='/save')

CORS(bp)


@bp.route('/settings', methods=(['POST']))
def settings():
    """updates the settings in both the file and backend"""
    data = request.json

    wheelRadius = data['wheelRad']
    camRatio = data['camRatio']
    fps = 18

    print(camRatio)

    if 'WHEEL_RADIUS' in os.environ:
        os.environ.pop('WHEEL_RADIUS')

    if (wheelRadius and wheelRadius > 0 and wheelRadius <= 20):
        os.environ['WHEEL_RADIUS'] = str(wheelRadius)
    else:
        os.environ['WHEEL_RADIUS'] = '3'

    if 'FPS' in os.environ:
        os.environ.pop('FPS')

    if (fps and fps > 1 and fps <= 60):
        os.environ['FPS'] = str(fps)
    else:
        os.environ['FPS'] = '10'

    if "CAM_RATIO" in os.environ:
        os.environ.pop('CAM_RATIO')

    if (camRatio and camRatio >= 0 and camRatio <= 0.5):
        os.environ['CAM_RATIO'] = str(camRatio)
    else:
        os.environ['CAM_RATIO'] = '0.2'

    with open("../.env", "w") as f:
        f.write("FPS={}\n".format(os.environ['FPS']))
        f.write("WHEEL_RADIUS={}\n".format(os.environ['WHEEL_RADIUS']))
        f.write("CAM_RATIO={}\n".format(os.environ['CAM_RATIO']))

    return jsonify({})


@bp.route('/newRun', methods=(['POST']))
def newRun():
    """Inserts a new run"""

    db = getDb()

    userInput = request.json

    name = userInput['Name']
    driverName = userInput['DriverName']
    tagged = userInput['Tagged']
    pipeID = userInput['PipeID']
    direction = userInput['Direction']
    lat = userInput['Lat']
    longi = userInput['Longi']
    tags = userInput['tags']
    error = None

    if not pipeID:
        error = 'PipeID is required.'
    elif not direction:
        error = 'Direction is required.'

    if error is None:

        checker = db.cursor(dictionary=True, buffered=True)
        query = ("SELECT * "
                 "FROM Pipe "
                 "WHERE Id = '{}'".format(pipeID))

        checker.execute(query)

        if(not checker.fetchall()):
            query = ("INSERT INTO Pipe (Id, Lat, Longi)"
                     "VALUES ('{}', {}, {})".format(
                         pipeID, lat, longi))
            sendCommand(db, query)

        checker.close()

        query = ("INSERT INTO Video (Name, PipeID, DriverName, DateTaken, Tagged, Direction) VALUES"
                 "('{}', '{}', '{}', NOW(), {}, '{}')".format(
                     name, pipeID, driverName, tagged, direction))
        videoID = sendCommand(db, query)
        videoData = getVideo(db, videoID)

        for tag in tags:
            query = ("INSERT INTO TaggedLocs (Position, Lat, Longi, Distance, VideoTime)"
                     "VALUES ({}, {}, {}, {}, {})".format(
                         tag["Position"], tag["Lat"], tag["Longi"], tag["Distance"], tag["VideoTime"]))
            tagID = sendCommand(db, query)

            query = ("INSERT INTO VideoToTags (VideoID, TagID)"
                     "VALUES ({}, {})".format(
                         videoID, tagID))
            print(query)
            sendCommand(db, query)

        moveFiles(videoData.get('PipeID'), str(
            videoData.get('DateTaken')).replace(' ', '_'))

        # add tags now

    return jsonify({})


@ bp.route('/editRun', methods=(['POST']))
def editRun():
    """edits a runs information"""
    db = getDb()
    userInput = request.json

    updateVideo(db, userInput["Id"], userInput["Name"],
                userInput["DriverName"], userInput["Tagged"], userInput["Direction"])
    return jsonify({})


@ bp.route('/editPin', methods=(['POST']))
def editPin():
    """edits a runs tagged status"""
    db = getDb()
    userInput = request.json

    query = ("UPDATE Video SET "
             "Tagged = {} "
             "WHERE Id = {} ".format(userInput["tagged"], userInput["id"]))

    sendCommand(db, query)

    return jsonify({})


def updateVideo(db, targ, name, driverName, tagged, direction):
    """updates information in the Video table"""
    query = ("UPDATE Video SET "
             "Name = '{}', DriverName = '{}', Tagged = {}, Direction = '{}' "
             "WHERE Id = {} ".format(name, driverName, tagged, direction, targ))

    sendCommand(db, query)


def updatePipe(db, targ, newName, lat, long):
    """updates the information in the pipe table"""
    query = (" UPDATE Pipe SET "
             "Id = '{}', Lat = {}, Longi = {} "
             "WHERE Id = '{}' ".format(newName, lat, long, targ))

    sendCommand(db, query)


def updateRoughLoc(db, targ, name, lat, long, rad):
    """updates rough location"""
    query = ("UPDATE RoughLocation "
             "Name = {}, Lat = {}, Longi = {}, Raduis = {} "
             "WHERE Id = {} ".format(name, lat, long, rad, targ))

    sendCommand(db, query)


# To be moved into a new files, and move it into a file

def sendCommand(db, query):
    """takes a query and then runs it. and commits the update.  also updates the most recently updated row"""
    update = db.cursor(dictionary=True, buffered=True)
    update.execute(query)
    value = update.lastrowid
    db.commit()
    update.close()

    # value is the value of the most recent created ID
    return value
