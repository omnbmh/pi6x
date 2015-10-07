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
* 引脚
* Arduino Uno
* 模拟输入 3 5 6 9 10 11
* 模拟输出 A0 A1 A2 A3 A4 A5
*
* 74HC595D 引脚
* pin 11 Clock Pin SH_CP 8
* pin 12 Latch Pin ST_CP 7
* pin 14 data pin DS 4
* Vcc pin 16 & MR pin 10 接 5V
* GND pin 8 & OE pin 13 接 地
*/

// #include
int ledPin = 13;

byte test595Data = B10111111;
int forwordData = 170; // 10101010
int backData = 85; // 01010101
int leftData = 102; // 01100110
int rightData = 153; // 10011001

int enable1Pin = 10; //M1 Speed Control
int enable2Pin = 9; //M2 Speed Control
int enable3Pin = 6; // M3 Speed Control
int enable4Pin = 5; // M4 Speed Control

int clockPin = 8;
int latchPin = 7; //
int dataPin = 3;



// 速度
int speed = 234;

void setMotorSpeed(int speed) {
  analogWrite(enable1Pin, speed);
  analogWrite(enable2Pin, speed);
  analogWrite(enable3Pin, speed);
  analogWrite(enable4Pin, speed);
}

void setup() {
  //Serial.begin(9600);
  pinMode(enable1Pin, OUTPUT);
  pinMode(enable2Pin, OUTPUT);
  pinMode(enable3Pin, OUTPUT);
  pinMode(enable4Pin, OUTPUT);

  // 设置 74HC595D 引脚
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  // light led
  pinMode(ledPin, OUTPUT);
}

void loop() {
  setMotorSpeed(speed);

  //shiftOut(test595Data);
  //for (int i = 0; i < 256 ; i++) {
  digitalWrite(latchPin, LOW);
  //shiftOut(i);
  shiftOut(forwordData);
  //shiftOut(test595Data);
  digitalWrite(latchPin, HIGH);
  //delay(1000);
  //}
  // light led
  digitalWrite(ledPin, HIGH);
}

void shiftOut(byte data) {


  boolean pinState ;
  digitalWrite(dataPin, LOW);
  digitalWrite(clockPin, LOW);
  for (int i = 0; i <= 7; i++) {
    digitalWrite(clockPin, LOW);
    if (data & (1 << i)) {
      pinState = HIGH;
    } else {
      pinState = LOW;
    }
    digitalWrite(dataPin, pinState);
    digitalWrite(clockPin, HIGH);
  }
  digitalWrite(clockPin, LOW);
}


