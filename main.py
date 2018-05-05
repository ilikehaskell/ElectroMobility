# connect to arduino
from CommandTypeEnum import CommandType
from PlatformState import PlatformState
from SerialHelper import SerialHelper
from rx.subjects import BehaviorSubject
from time import sleep
from DirectionEnum import Direction
from flask import Flask
from flask_socketio import SocketIO, emit

DEFAULT_STEERING_POSITION = 100
DEFAULT_THROTTLE_POSITION = 90
DEFAULT_LEFT = 140
DEFAULT_RIGHT = 60
DEFAULT_FORWARD = 100
DEFAULT_BACKWARDS = 0

serialHelper = SerialHelper()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
    
@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

def handleMessage(message):
    print(message)
    
def writeSteering(angle):
    serialHelper.write("{0} {1}".format(CommandType.Steering, angle))

def writeThrottle(throttle):
    serialHelper.write("{0} {1}".format(CommandType.Throttle, throttle))

def setThrottle(throttle):
    currentThrottle = throttle

def getThrottle():
    return currentThrottle

currentAngle = DEFAULT_STEERING_POSITION
currentThrottle = 0

serialHelper.messages.subscribe(handleMessage)

#sleep(5)  # Time in seconds.
#message = "{0} {1}".format(CommandType.Steering, command)
#print(message)
#serialHelper.write(message)

@socketio.on('move')
def test_message(message):
    if message["data"] == 'left':
	currentAngle += 10
	writeAngle(currentAngle)
        emit('answer', {'data': currentAngle})

    if message["data"] == 'right':
	currentAngle -= 10
	writeAngle(currentAngle)
        emit('answer', {'data': currentAngle})
    if message["data"] == 'forward':
        setThrottle(100)
    	writeThrottle(100)
	emit('answer', {'data': 100})
    if message["data"] == 'backwards':
    	setThrottle(0)
    	writeThrottle(0)
    	emit('answer', {'data': 0})        
    socketio.sleep(0)
    
socketio.run(app, host='0.0.0.0')

