int latchPin = 7; // 74HC595 12
int clockPin = 8;// 74HC595 11
int dataPin = 3;// 74HC595 14

void setup() {
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
}

void loop() {
  for (int i = 0; i < 256 ; i++) {
    digitalWrite(latchPin, LOW);
    shiftOut(i);
    digitalWrite(latchPin, HIGH);
    delay(1000);
  }
}

void shiftOut(byte data) {
  boolean pinState;
  digitalWrite(dataPin, LOW);
  digitalWrite(clockPin, LOW);
  for (int i = 0; i <= 7; i++) {
    digitalWrite(clockPin, LOW);
    if (data & (1 << i)) {
      pinState = HIGH;
    }
    else {
      pinState = LOW;
    }
    digitalWrite(dataPin, pinState);
    digitalWrite(clockPin, HIGH);
  }
  digitalWrite(clockPin, LOW);
}

