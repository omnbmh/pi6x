int ledDelay = 10000;

int redPin = 10;
int yellowPin = 9;
int greenPin = 8;

void setup(){
  pinMode(redPin,OUTPUT);
  pinMode(yellowPin,OUTPUT);
  pinMode(greenPin,OUTPUT);
}

void loop(){
  digitalWrite(redPin,HIGH);
  delay(ledDelay);

  digitalWrite(yellowPin,HIGH);
  digitalWrite(redPin,LOW);
  delay(2000);
  digitalWrite(greenPin,HIGH);
  digitalWrite(redPin,LOW);
  digitalWrite(yellowPin,LOW);
  delay(ledDelay);

  digitalWrite(yellowPin,HIGH);
  digitalWrite(greenPin,LOW);
  delay(2000);
  digitalWrite(yellowPin,LOW);
}






