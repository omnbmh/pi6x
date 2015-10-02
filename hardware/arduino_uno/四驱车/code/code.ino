/*
* 四驱车代码
*/
int enable1Pin = 11;
int enable2Pin = 10;
int in1Pin = 8;
int in2Pin = 9;
int in3Pin = 5;
int in4Pin = 7;

// 调整速度
int potPin = 0;

// 速度
int speed = 0;
// 方向
boolean direction = 0;

void setMotor(int speed, boolean reverse){
  analogWrite(enable1Pin, 230);
  analogWrite(enable2Pin, 230);
  //digitalWrite(enable1Pin,HIGH);
  //digitalWrite(enable2Pin,HIGH);
  digitalWrite(in1Pin, HIGH);
  digitalWrite(in2Pin, LOW);
  digitalWrite(in3Pin, HIGH);
  digitalWrite(in4Pin, LOW);
}

void setup(){
  //Serial.begin(9600);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(in3Pin, OUTPUT);
  pinMode(in4Pin, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  pinMode(enable2Pin, OUTPUT);
  // light led
  pinMode(13, OUTPUT);
}

void loop(){
  //int speed = analogRead(potPin)/4;
  // 设置 电机的速度 和 方向
  setMotor(speed,direction);
  //delay(1000);
  // light led
  digitalWrite(13, HIGH);
}



