/*
* 四驱车代码 －单电机
*/
int enablePin = 11; // pwm
int in1Pin = 8;
int in2Pin =9;

// 速度
int speed = 234;

void setMotor() {
  analogWrite(enablePin, speed);
  //digitalWrite(enable1Pin,HIGH);
  digitalWrite(in1Pin, HIGH);
  digitalWrite(in2Pin, LOW);
}

void setup() {
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(enablePin, OUTPUT);
  // light led
  pinMode(13, OUTPUT);
}

void loop() {
  // 设置 电机的速度 和 方向
  setMotor();
  // light led
  digitalWrite(13, HIGH);
}



