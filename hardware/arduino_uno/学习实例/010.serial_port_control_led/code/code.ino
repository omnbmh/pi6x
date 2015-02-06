char buffer[18];

int ledRed =11;
int ledGreen =10;
int ledBlue =9;

void setup(){
  Serial.begin(9600);
  Serial.flush();
  pinMode(ledRed,OUTPUT);
  pinMode(ledGreen,OUTPUT);
  pinMode(ledBlue,OUTPUT);
}

void loop(){
  if(Serial.available() > 0){
    int index =0;
    delay(100);
    int numChar = Serial.available();
    if (numChar >15){
      numChar = 15;
    }
    while(numChar--){
      buffer[index++] = Serial.read();
    }
    splitString(buffer);
  }
}

void splitString(char* data){
  Serial.print("Data entered: ");
  Serial.println(data);
  char* parameter;
  parameter = strtok(data, " ,");
  while(parameter != NULL){
    setLed(parameter);
    parameter = strtok(NULL," ,");
  }
  // clear text
  for(int i =0; i<16;i++){
    buffer[i] = '\0';
  }
  Serial.flush();
}

void setLed(char* data){
  if((data[0] == 'r') || (data[0] == 'R')){
    int ans = strtol(data+1,NULL,10);
    ans = constrain(ans,0,255);
    analogWrite(ledRed,ans);
    Serial.print("Red is set to: ");
    Serial.println(ans);
  }
  if((data[0] == 'g') || (data[0] == 'G')){
    int ans = strtol(data+1,NULL,10);
    ans = constrain(ans,0,255);
    analogWrite(ledGreen,ans);
    Serial.print("Green is set to: ");
    Serial.println(ans);
  }
  if((data[0] == 'b') || (data[0] == 'B')){
    int ans = strtol(data+1,NULL,10);
    ans = constrain(ans,0,255);
    analogWrite(ledBlue,ans);
    Serial.print("Blue is set to: ");
    Serial.println(ans);
  }
}






