# connect to arduino
from PlatformState import PlatformState
from SerialHelper import SerialHelper
from rx.subjects import BehaviorSubject

from DirectionEnum import Direction

def initialState():
    return PlatformState(0, 0, Direction.Forward)

def handleMessage(message):
    print(message)

def core():
    serialHelper = SerialHelper()
    currentPlatformState = BehaviorSubject(initialState())

    serialHelper.messages.subscribe(handleMessage)
core()
x = 0
while x < 100:
    print('from main: ${1}', x)
    x += 1