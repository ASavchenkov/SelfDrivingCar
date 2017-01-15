
enum Drive {forward, nuetral, reverse};
String currentCommand = "";
int leftRelay = 10, rightRelay = 11;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Connected.");
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

void steerControl(int angle){
  //TODO
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
  delay(1000);
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
  String nextCommand = "";
  if(Serial.available()){
    char letter = Serial.read();
    if(letter == 'q'){
        nextCommand = currentCommand;
        currentCommand = "";
    } else {
      currentCommand.concat(letter);
    }
  }
  processCommand(nextCommand);
}
