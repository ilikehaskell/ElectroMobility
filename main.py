# connect to arduino
from CommandTypeEnum import CommandType
from PlatformState import PlatformState
from SerialHelper import SerialHelper
from rx.subjects import BehaviorSubject
from time import sleep
from DirectionEnum import Direction

DEFAULT_STEERING_POSITION = 100
DEFAULT_THROTTLE_POSITION = 90
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('move')
def test_message(message):
    print(message)
    emit('answer', {'data': message})
    socketio.sleep(0)
    
@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

def initialState():
    return PlatformState(DEFAULT_STEERING_POSITION, DEFAULT_THROTTLE_POSITION, Direction.Forward)

def handleMessage(message):
    print(message)

serialHelper = SerialHelper()
currentPlatformState = BehaviorSubject(initialState())

serialHelper.messages.subscribe(handleMessage)

command = currentPlatformState.value.steering + 10

#sleep(5)  # Time in seconds.
#message = "{0} {1}".format(CommandType.Steering, command)
#print(message)
#serialHelper.write(message)

socketio.run(app, host='0.0.0.0')

