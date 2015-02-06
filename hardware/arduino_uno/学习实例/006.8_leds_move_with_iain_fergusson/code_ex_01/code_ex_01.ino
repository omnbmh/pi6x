byte ledPin[] = {
  6,7,8,9,10,11,12,13};
int ledDelay;
int dre =1;
int currentLed = 0;
unsigned long changeTime;

int potPin = 2;

void setup(){
  for(int x = 0;x<8;x++){
    pinMode(ledPin[x],OUTPUT);
  }
  changeTime = millis();
}
void loop(){
  ledDelay = analogRead(potPin);
  if ((millis() - changeTime) > ledDelay){
    changeLed();
    changeTime = millis();
  }
}
void changeLed(){
  for(int i =0; i<8;i++){
    digitalWrite(ledPin[i],LOW);
  }
  digitalWrite(ledPin[currentLed],HIGH);
  digitalWrite(ledPin[7-currentLed],HIGH);
  currentLed += dre;
  if (currentLed==3){
    dre = -1;
  }
  if (currentLed==0){
    dre = 1;
  }
}


