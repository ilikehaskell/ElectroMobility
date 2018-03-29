# connect to arduino
from CommandTypeEnum import CommandType
from PlatformState import PlatformState
from SerialHelper import SerialHelper
from rx.subjects import BehaviorSubject
from time import sleep
from DirectionEnum import Direction

DEFAULT_STEERING_POSITION = 100
DEFAULT_THROTTLE_POSITION = 90

def initialState():
    return PlatformState(DEFAULT_STEERING_POSITION, DEFAULT_THROTTLE_POSITION, Direction.Forward)

def handleMessage(message):
    print(message)

def core():
    serialHelper = SerialHelper()
    currentPlatformState = BehaviorSubject(initialState())

    serialHelper.messages.subscribe(handleMessage)

    command = currentPlatformState.value.steering + 10

    sleep(5)  # Time in seconds.
    message = "{0} {1}".format(CommandType.Steering, command)
    print(message)
    serialHelper.write(message)

core()
