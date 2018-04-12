#include <Servo.h> 
#define trigPin1 3
#define echoPin1 2
#define trigPin2 4
#define echoPin2 5
#define trigPin3 7
#define echoPin3 8

long duration, distance, RightSensor,BackSensor,FrontSensor,LeftSensor;

Servo throttleServo;
Servo steeringServo;

int throttlePin = 9;
int steeringPin = 10;
int minPulseRate = 1000;
int maxPulseRate = 2000;
int throttleChangeDelay = 10;
int steeringChangeDelay = 10;

enum Event {
  STEERING = 1,
  THROTTLE = 2
};

void setup() {
  
  Serial.begin(115200);
  Serial.setTimeout(500);
  
  // Attach the the servo to the correct pin and set the pulse range
  throttleServo.attach(throttlePin, minPulseRate, maxPulseRate);
  steeringServo.attach(steeringPin);
  // Write a minimum value (most ESCs require this correct startup)
  throttleServo.write(0);
  steeringServo.write(0);  
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(trigPin3, OUTPUT);
  pinMode(echoPin3, INPUT);
}

void loop() {
  // Wait for some input
  if (steeringServo.read() == 0) {
    steeringServo.write(100);
  }
  
  if (Serial.available() > 0) {

    Event e = static_cast<Event>(Serial.parseInt());
    
    int newValue = Serial.parseInt();
    switch (e) {
      case STEERING:
        setSteering2(normalizeServo(newValue));
      break;
      case THROTTLE:
        changeThrottle2(normalizeServo(newValue));
      break;
      default:
      break;
    }
  }
  
  SonarSensor(trigPin1, echoPin1);
  RightSensor = distance;
  SonarSensor(trigPin2, echoPin2);
  FrontSensor = distance;
  SonarSensor(trigPin3, echoPin3);
  LeftSensor = distance;
  
  Serial.print(LeftSensor);
  Serial.print(" - ");
  Serial.print(FrontSensor);
  Serial.print(" - ");
  Serial.println(RightSensor);

  if (LeftSensor < 30 || FrontSensor < 30 || RightSensor < 30) {
    changeThrottle2(0);
  }
}

void SonarSensor(int trigPin,int echoPin)
{
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
duration = pulseIn(echoPin, HIGH);
distance = (duration/2) / 29.1;
}

void setSteering2(int angle) {
  steeringServo.write(angle);
}

void changeThrottle2(int angle) {
  throttleServo.write(angle);
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
            Serial.println(throttle);

  return throttle;
}

int readSteeringAngle() {
  int angle = steeringServo.read();
          Serial.println(angle);

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
