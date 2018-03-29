from DirectionEnum import Direction

class PlatformState:

    steering = 0
    throttle = 0
    direction = Direction.Forward

    def __init__(self, steering, throttle, direction):
        self.steering = steering
        self.throttle = throttle
        self.direction = direction