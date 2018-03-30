#include <Servo.h> 

Servo throttleServo;
Servo steeringServo;

int throttlePin = 9;
int steeringPin = 10;
int minPulseRate = 1000;
int maxPulseRate = 2000;
int throttleChangeDelay = 10;
int steeringChangeDelay = 10;

const int STEERING_CENTER_VALUE = 100;

enum Event {
  STEERING = 1,
  THROTTLE = 2
};

void setup() {
  
  Serial.begin(9600);
  Serial.setTimeout(500);
  
  // Attach the the servo to the correct pin and set the pulse range
  throttleServo.attach(throttlePin, minPulseRate, maxPulseRate);
  steeringServo.attach(steeringPin);
  // Write a minimum value (most ESCs require this correct startup)
  throttleServo.write(0);
  steeringServo.write(0);  
}

void loop() {
  // Wait for some input
  if (steeringServo.read() == 0)
    setSteering(STEERING_CENTER_VALUE);
  if (Serial.available() > 0) {

    Event e = static_cast<Event>(Serial.parseInt());
    
    Serial.print(e);
    int newValue = Serial.parseInt();
    switch (e) {
      case STEERING:
        setSteering(normalizeServo(newValue));
        Serial.print(newValue);
      break;
      case THROTTLE:
        Serial.print(newValue);
        changeThrottle(normalizeServo(newValue));
      break;
      default:
      break;
    }
  }

}

void setSteering(int angle) {
  int currentAngle = readSteeringAngle();
  
  // Are we going up or down?
  int step = 1;
  if( angle < currentAngle )
    step = -1;
  
  // Slowly move to the new throttle value 
  while( currentAngle != angle ) {
    steeringServo.write(currentAngle + step);
    currentAngle = readSteeringAngle();
    delay(steeringChangeDelay);
  }
}

void changeThrottle(int throttle) {
  
  // Read the current throttle value
  int currentThrottle = readThrottle();
  
  // Are we going up or down?
  int step = 1;
  if( throttle < currentThrottle )
    step = -1;
  
  // Slowly move to the new throttle value 
  while( currentThrottle != throttle ) {
    throttleServo.write(currentThrottle + step);
    currentThrottle = readThrottle();
    delay(throttleChangeDelay);
  }
  
}

int readThrottle() {
  int throttle = throttleServo.read();

  return throttle;
}

int readSteeringAngle() { // steering angle between 60 (left) 100 (forward) and 140 (right)
  int angle = steeringServo.read();

  return angle;
}

// Ensure the servo value is between 0 - 180
int normalizeServo(int value) {
  if( value < 0 )
    return 0;
  if( value > 180 )
    return 180;
  return value;
}
