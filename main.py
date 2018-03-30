# connect to arduino
from CommandTypeEnum import CommandType
from PlatformState import PlatformState
from SerialHelper import SerialHelper
from rx.subjects import BehaviorSubject
from time import sleep
from DirectionEnum import Direction

DEFAULT_STEERING_POSITION = 100
DEFAULT_THROTTLE_POSITION = 90
DEFAULT_LEFT = 140
DEFAULT_RIGHT = 60
DEFAULT_FORWARD = 100
DEFAULT_BACKWARDS = 0
from flask import Flask
from flask_socketio import SocketIO, emit

serialHelper = SerialHelper()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
    
@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

def initialState():
    return PlatformState(DEFAULT_STEERING_POSITION, DEFAULT_THROTTLE_POSITION, Direction.Forward)

def handleMessage(message):
    print(message)
    
def stateHandler(platformState):
    serialHelper.write("{0} {1}".format(CommandType.Steering, platformState.steering))
    sleep(0.7)
    serialHelper.write("{0} {1}".format(CommandType.Throttle, platformState.throttle))
    print('answer', platformState.steering)



currentPlatformState = BehaviorSubject(initialState())

serialHelper.messages.subscribe(handleMessage)

x = currentPlatformState.subscribe(stateHandler)

#sleep(5)  # Time in seconds.
#message = "{0} {1}".format(CommandType.Steering, command)
#print(message)
#serialHelper.write(message)

@socketio.on('move')
def test_message(message):
    if message["data"] == 'left':
        currentPlatformState.on_next(PlatformState(currentPlatformState.value.steering + 20, currentPlatformState.value.throttle, currentPlatformState.value.direction))
        emit('answer', {'data': currentPlatformState.value.steering})

    if message["data"] == 'right':
        currentPlatformState.on_next(PlatformState(currentPlatformState.value.steering - 20, currentPlatformState.value.throttle, currentPlatformState.value.direction))
    if message["data"] == 'forward':
        currentPlatformState.on_next(PlatformState(currentPlatformState.value.steering, 100, currentPlatformState.value.direction))
    if message["data"] == 'backwards':
        currentPlatformState.on_next(PlatformState(currentPlatformState.value.steering, 0, currentPlatformState.value.direction))
    emit('answer', {'data': currentPlatformState.value.throttle})
    socketio.sleep(0)
    
socketio.run(app, host='0.0.0.0')

