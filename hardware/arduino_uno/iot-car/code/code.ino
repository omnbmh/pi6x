/*
* 微型物联网－四驱车
*
* 这个程序使用74H595D驱动了4个电机的正反转 使用L293D驱动四个电机的速度
*
* L293D ＊ 2
* 74HC595D ＊ 1
* Create 2015年09月28日
* Modified 2015年10月07日
* by 陈德志
*
*/

// #include

int forwordData = 170; // 10101010
int backData = 85; // 01010101
int leftData = 102; // 01100110
int rightData = 153; // 10011001

int enable1Pin = 11; //M1 Speed Control
int enable2Pin = 10; //M2 Speed Control
int enable3Pin = 9; // M3 Speed Control
int enable4Pin = 8; // M4 Speed Control

int latchPin = 7;
int dataPin = 6;
int clockPin = 5;



// 调整速度
int potPin = 0;

void setMotor() {
  analogWrite(enable1Pin, 230);
  analogWrite(enable2Pin, 230);
  analogWrite(enable3Pin, 230);
  analogWrite(enable4Pin, 230);
}

void setup() {
  //Serial.begin(9600);
  pinMode(enable1Pin, OUTPUT);
  pinMode(enable2Pin, OUTPUT);
  pinMode(enable3Pin, OUTPUT);
  pinMode(enable4Pin, OUTPUT);
  // light led
  pinMode(13, OUTPUT);
}

void loop() {
  //int speed = analogRead(potPin)/4;
  // 设置 电机的速度 和 方向
  setMotor();
  //delay(1000);
  // light led
  digitalWrite(13, HIGH);
}

void shiftOut(byte data) {
  digitalWrite(dataPin, LOW);
  digitalWrite(clockPin, LOW);
  for (int i = 0; i <= 7; i++) {
    digitalWrite(clockPin, LOW);
    if (data & (1 << i)) {
      digitalWrite(dataPin, HIGH);
    } else {
      digitalWrite(dataPin, LOW);
    }
    digitalWrite(clockPin, LOW);
  }
}


