#include <IRremote.h>
// pwm chongtu 6 and 11
int RECV_PIN = 11;
int enablePin = 6;
int in1Pin = 10;
int in2Pin = 9;

#define qian 0x00FF02FD
#define hou 0x00FF22DD
#define ting 0x00FFC23D
#define jia 0x00FFA857
#define jian 0x00FFE01F
#define auto 0x00FF906F

int speed = 0;
int speedstep = 30;
boolean direction = 0;// true qian

IRrecv irrecv(RECV_PIN);
decode_results results;

void dump(decode_results *results) {
  int count = results->rawlen;
  if (results->decode_type == UNKNOWN){
     Serial.println("Could not decode message");
   } 
  else{
    if (results->decode_type == NEC){
       Serial.print("Decoded NEC: ");
    } 
    else if (results->decode_type == SONY) {
       Serial.print("Decoded SONY: ");
    } 
    else if (results->decode_type == RC5){
       Serial.print("Decoded RC5: ");
    } 
    else if (results->decode_type == RC6){
       Serial.print("Decoded RC6: ");
    }
    Serial.print(results->value, HEX);
    Serial.print(" (");
    Serial.print(results->bits, DEC);
    Serial.println(" bits)");
   }
   Serial.print("Raw (");
   Serial.print(count, DEC);
   Serial.print("): ");

  for (int i = 0; i < count; i++) 
  {
      if ((i % 2) == 1) {
        Serial.print(results->rawbuf[i]*USECPERTICK, DEC);
      } 
      else{
        Serial.print(-(int)results->rawbuf[i]*USECPERTICK, DEC);
      }
      Serial.print(" ");
  }
  Serial.println("");
}

void setMotor(int speed, boolean reverse){
  Serial.print("speed: ");
  Serial.println(speed);
  Serial.print("reverse: ");
  Serial.println(reverse);
  
  analogWrite(enablePin, speed);
  digitalWrite(in1Pin, !reverse);
  digitalWrite(in2Pin, reverse);
}


void qianFunc(){
  if(speed <= 0){
    speed = 100;
  }
  direction = 0;
  setMotor(speed,direction);
}
void houFunc(){
  if(speed <= 0){
    speed = 100;
  }
  direction = 1;
  setMotor(speed,direction);
}

void tingFunc(){
  if(speed == 0){
    setMotor(100,direction);
  }
  else{
    setMotor(0,direction);
  }
}

void autoFunc(){
  setMotor(250,direction);
}

void jiaFunc(){
  if(speed <= 255){
    speed += speedstep;
  }
  else{
    speed = 255;
  }
  setMotor(speed,direction);
}

void jianFunc(){
  if(speed >= 0){
    speed -= speedstep;
  }
  else{
    speed = 0;
  }
  setMotor(speed,direction);
}


void setup(){
  pinMode(RECV_PIN, INPUT);   
  
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(enablePin, OUTPUT);
  
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  
  irrecv.enableIRIn(); // Start the receiver
}

int on = 0;
unsigned long last = millis();

void loop(){
  //setMotor(250,0);
   
  if (irrecv.decode(&results)){
    if (millis() - last > 250){
       on = !on;
       digitalWrite(13, on ? HIGH : LOW);
       dump(&results);
    }
    /*
    if (results.value == auto){
      autoFunc();
    }
   */
    switch(results.value){
      case qian:
        qianFunc();
        break;
      case hou:
        houFunc();
        break;
      case ting:
        tingFunc();
        break;
      case jia:
        jiaFunc();
        break;
      case jian:
        jianFunc();
        break;
      case auto:
        autoFunc();
        break;
      default:
         autoFunc(); 
         break;
    }
    
    //delay(600);      
    last = millis();      
    irrecv.resume(); // Receive the next value
  }
}


