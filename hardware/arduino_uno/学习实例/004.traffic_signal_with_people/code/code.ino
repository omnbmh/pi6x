int carRed = 12;
int carYellow = 11;
int carGreen = 10;

int pedRed = 9;
int pedGreen = 8;

int btn = 2;
int crossTime = 5000;
unsigned long changeTime = 0;

void setup(){
  Serial.begin(9600);
  pinMode(carRed,OUTPUT);
  pinMode(carYellow,OUTPUT);
  pinMode(carGreen,OUTPUT);
  pinMode(pedRed,OUTPUT);
  pinMode(pedGreen,OUTPUT);
  pinMode(btn,INPUT);

  digitalWrite(carGreen,HIGH);
  digitalWrite(pedRed,HIGH);
}

void loop(){
  int state = digitalRead(btn);
  if (state == HIGH && (millis() - changeTime) > 5000){
    Serial.println(state);
    changeLights();
  }

}

void changeLights(){
  digitalWrite(carGreen,LOW);
  digitalWrite(carYellow,HIGH);
  delay(2000);

  digitalWrite(carYellow,LOW);
  digitalWrite(carRed,HIGH);
  delay(1000);
  digitalWrite(pedRed,LOW);
  digitalWrite(pedGreen,HIGH);
  delay(crossTime);

  for(int x = 0; x<10;x++){
    digitalWrite(pedGreen,HIGH);
    delay(200);
    digitalWrite(pedGreen,LOW);
    delay(200);
  }
  digitalWrite(pedRed,HIGH);
  delay(500);
  digitalWrite(carYellow,HIGH);
  digitalWrite(carRed,LOW);
  delay(1000);
  digitalWrite(carGreen,HIGH);
  digitalWrite(carYellow,LOW);

  changeTime = millis();
}











