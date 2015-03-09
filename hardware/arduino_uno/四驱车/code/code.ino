/*
* 四驱车代码
*/
int enablePin = 11;
int in1Pin = 10;
int in2Pin = 9;

int speed = 20;
boolean direction = 0;

void setMotor(int speed, boolean reverse){
  analogWrite(enablePin, speed);
  digitalWrite(in1Pin, !reverse);
  digitalWrite(in2Pin, reverse);
}

void setup(){
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(enablePin, OUTPUT);
  
  pinMode(13, OUTPUT);
}

void loop(){
  setMotor(speed,direction);
  digitalWrite(13, HIGH);
}



