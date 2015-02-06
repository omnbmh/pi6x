byte ledPin[] = {
  6,7,8,9,10,11,12,13};
int ledDelay;
int hight = 7;
int ground = 0;
int dre = -1;
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
  if((millis() - changeTime) > ledDelay){
    changeLed();
    changeTime = millis();
  }
}
void changeLed(){
  for(int i = 0; i < 8; i++){
    digitalWrite(ledPin[i],LOW);
  }
  if(ground ==0){
    digitalWrite(ledPin[hight],HIGH);
    hight += dre;
    if(hight >= 7){
      dre = -1;
    }
    if(hight <= 0)
    {
      hight = 7;
    }
    ground= 1;
  }
  else{
    digitalWrite(ledPin[0],HIGH);
    ground= 0;
  }
}








