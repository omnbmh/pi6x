int ledPin =11;
float sinVal;
int ledVal;

void setup(){
  pinMode(ledPin,OUTPUT);
}

void loop(){
  for(int i = 0;i<180;i++){
    sinVal=(sin(i*(3.1412/180)));
    ledVal = int(sinVal*255);
    analogWrite(ledPin,ledVal);
    delay(25);
  }
}

