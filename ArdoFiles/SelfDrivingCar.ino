#include <Servo.h>

enum Drive {forward, nuetral, reverse};
String currentCommand = "";
int leftRelay = 10, rightRelay = 11;
//A5, D6
int steerPOD = 5, motorPin = 6;;
Servo motor;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Connected.");
  //digitalWrite(7,LOW);
  pinMode(leftRelay , OUTPUT);
  pinMode(rightRelay , OUTPUT);
  motor.attach(motorPin);
  digitalWrite(leftRelay, HIGH);
  digitalWrite(rightRelay, HIGH);
}


String driveToString(Drive d){
  switch(d){
    case forward:
      return "forward";
    case nuetral:
      return "nuetral";
    case reverse:
      return "reverse";
    defualt:
      return "park";
  }
}
int toAngle(int pos){
  //945-1023
  // 0(0) to 5(1023)
  int x = (90*(pos-945)/78)-45;
  return x;
}

void steerControl(int desiredAngle){
  int currentPos = analogRead(steerPOD);
  int currentAngle = toAngle(currentPos);
  float pgain = 0.06;
  float delta = pgain*(desiredAngle - currentAngle);
  if(delta > 1.0){
    delta = 1;
  } else if (delta < -1){
    delta = -1; 
  }
  motor.write(90*delta+90);
  Serial.println(90*delta+90);
}

void driveControl(Drive d){
  switch(d){
    case forward:
      digitalWrite(leftRelay, LOW);
      digitalWrite(rightRelay, HIGH);
      break;
    case reverse:
      digitalWrite(leftRelay, HIGH);
      digitalWrite(rightRelay, LOW);
      break;
    case nuetral:
    default:
      digitalWrite(leftRelay, LOW);
      digitalWrite(rightRelay, LOW);
  }
}

void driveTrain(Drive d, int angle){
  driveControl(d);
  steerControl(angle);
  Serial.println(driveToString(d));
  Serial.println(angle);
  delay(500);
}

void processCommand(String com){
  if(com == "") return;
  int angle = com.substring(1).toInt();
  Drive drive;
  switch(com.charAt(0)){
    case 'f':
    case 'F':
      drive = forward;
      break;
    case 'n':
    case 'N':
      drive = nuetral;
      break;
    case 'r':
    case 'R':
      drive = reverse;
      break;
    default:
      drive = nuetral;  
  }
  driveTrain(drive, angle);
}

void loop() {
  // put your main code here, to run repeatedly:
    
  /*String nextCommand = "";
  if(Serial.available()){
    char letter = Serial.read();
    if(letter == 'q'){
        nextCommand = currentCommand;
        currentCommand = "";
    } else {
      currentCommand.concat(letter);
    }
  }*/
  
  processCommand("F0");
}
