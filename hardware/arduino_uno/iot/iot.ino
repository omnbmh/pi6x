#define SEG_A 2
#define SEG_B 3
#define SEG_C 4
#define SEG_D 5
#define SEG_E 6
#define SEG_F 7
#define SEG_G 8
#define SEG_H 9

#define COM1 10
#define COM2 11
#define COM3 12
#define COM4 13

byte segs[8] = {SEG_A, SEG_B, SEG_C, SEG_D, SEG_E, SEG_F, SEG_G, SEG_H };

unsigned char table[10][8] = {
	{0,	0,	1,	1,	1,	1,	1,	1},			//0
	{0,	0,	0,	0,	0,	1,	1,	0},			//1
	{0,	1,	0,	1,	1,	0,	1,	1},			//2
	{0,	1,	0,	0,	1,	1,	1,	1},			//3
	{0,	1,	1,	0,	0,	1,	1,	0},			//4
	{0,	1,	1,	0,	1,	1,	0,	1},			//5
	{0,	1,	1,	1,	1,	1,	0,	1},			//6
	{0,	0,	0,	0,	0,	1,	1,	1},			//7
	{0,	1,	1,	1,	1,	1,	1,	1},			//8
	{0,	1,	1,	0,	1,	1,	1,	1}			//9
};

int potPin = 0;

void setup(){
  pinMode(SEG_A,OUTPUT);		//设置为输出引脚
  pinMode(SEG_B,OUTPUT);
  pinMode(SEG_C,OUTPUT);
  pinMode(SEG_D,OUTPUT);
  pinMode(SEG_E,OUTPUT);
  pinMode(SEG_F,OUTPUT);
  pinMode(SEG_G,OUTPUT);
  pinMode(SEG_H,OUTPUT);

  pinMode(COM1,OUTPUT);
  pinMode(COM2,OUTPUT);
  pinMode(COM3,OUTPUT);
  pinMode(COM4,OUTPUT);
  Serial.begin(9600);
}

void loop(){
  int val = analogRead(potPin);
  int dat = (125*val)>>8;
  Serial.print("t:");
  Serial.println(dat);
  //delay(600000);
  int number = dat;
  //for (unsigned int number = 0; number < 10000; number++){
    unsigned long startTime = millis();
    for (unsigned long elapsed = 0; elapsed < 10000; elapsed = millis() - startTime){  
      displayDigital(4, number%10);
      delay(1);
      displayDigital(3, (number/10)%10);
      delay(1);
      displayDigital(2, (number/100)%10);
      delay(1);
      displayDigital(1, (number/1000)%10);
      delay(1);
    }
  //}
}

//
void displayDigital(int digital, byte number){
  digitalWrite(COM1, HIGH);
  digitalWrite(COM2, HIGH);
  digitalWrite(COM3, HIGH);
  digitalWrite(COM4, HIGH);
  
  switch(digital){
    case 1: digitalWrite(COM1, LOW); break;
    case 2: digitalWrite(COM2, LOW); break;
    case 3: digitalWrite(COM3, LOW); break;
    case 4: digitalWrite(COM4, LOW); break;
  }
  
  digitalWrite(SEG_A,LOW);			//去除余晖
  digitalWrite(SEG_B,LOW);
  digitalWrite(SEG_C,LOW);
  digitalWrite(SEG_D,LOW);
  digitalWrite(SEG_E,LOW);
  digitalWrite(SEG_F,LOW);
  digitalWrite(SEG_G,LOW);
  digitalWrite(SEG_H,LOW);
  
  for (int i = 0; i < 8; i++){
    digitalWrite(segs[i], table[number][7-i]);//look table
  }
}
