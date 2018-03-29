import serial
import threading
from rx.subjects import BehaviorSubject


def worker(serialHelper):
    # while serialHelper.ser.in_waiting:
    #     serialHelper.setMessage(serialHelper.ser.readline())
    i = 0
    while i < 100:
        serialHelper.setMessage(i)
        i += 1
    return

class SerialHelper:
    ser = serial.Serial('/dev/ttyACM0', 9600)
    def __init__(self):
        self.messages = BehaviorSubject("")
        self.read()

    # def read(self, recieved):
    #     while self.ser.in_waiting:
    #         recieved(self.ser.readline())
    #



    def read(self):
        self.threadObj = threading.Thread(target=worker, args=(self,))
        self.threadObj.start()

    def setMessage(self, message):
        self.messages.on_next(message)
