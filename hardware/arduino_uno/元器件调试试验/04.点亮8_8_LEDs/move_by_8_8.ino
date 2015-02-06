#define display_array_size 8
//ascii 8*8 dot font
#define data_null 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 // all lights off
#define data_ascii_A 0x02, 0x0C, 0x18, 0x68, 0x68, 0x18, 0x0C, 0x02 /*"A",0*/

byte data_ascii[][display_array_size] = {
  data_null,
  data_ascii_A,
};

const int row1 = 2; // the number of the row pin 9 
const int row2 = 3; // the number of the row pin 14 
const int row3 = 4; // the number of the row pin 8 
const int row4 = 5; // the number of the row pin 12 
const int row5 = 17; // the number of the row pin 1 
const int row6 = 16; // the number of the row pin 7 
const int row7 = 15; // the number of the row pin 2 
const int row8 = 14; // the number of the row pin 5 
//the pin to control COl 
const int col1 = 6; // the number of the col pin 13 
const int col2 = 7; // the number of the col pin 3 
const int col3 = 8; // the number of the col pin 4 
const int col4 = 9; // the number of the col pin 10 
const int col5 = 10; // the number of the col pin 6 
const int col6 = 11; // the number of the col pin 11 
const int col7 = 12; // the number of the col pin 15 
const int col8 = 13; // the number of the col pin 16 

void displayLed(byte row,byte col){
  //set for variable
  int j;
  //set all pin low
  byte temp = row;
  for (j=2;j<6;j++){
    digitalWrite(j,LOW);
  }
  digitalWrite(row5, LOW);
  digitalWrite(row6, LOW);
  digitalWrite(row7, LOW);
  digitalWrite(row8, LOW);
  for (j=6;j<14;j++){
    digitalWrite(j,HIGH);
  }


  switch(col)
  {
  case 1: 
    digitalWrite(col1, LOW); 
    break;
  case 2: 
    digitalWrite(col2, LOW); 
    break;
  case 3: 
    digitalWrite(col3, LOW); 
    break;
  case 4: 
    digitalWrite(col4, LOW); 
    break;
  case 5: 
    digitalWrite(col5, LOW); 
    break;
  case 6: 
    digitalWrite(col6, LOW); 
    break;
  case 7: 
    digitalWrite(col7, LOW); 
    break;
  case 8: 
    digitalWrite(col8, LOW); 
    break;
  default: 
    break;
  }

  switch(row)
  {
  case 1: 
    digitalWrite(row1, HIGH); 
    break;
  case 2: 
    digitalWrite(row2, HIGH); 
    break;
  case 3: 
    digitalWrite(row3, HIGH); 
    break;
  case 4: 
    digitalWrite(row4, HIGH); 
    break;
  case 5: 
    digitalWrite(row5, HIGH); 
    break;
  case 6: 
    digitalWrite(row6, HIGH); 
    break;
  case 7: 
    digitalWrite(row7, HIGH); 
    break;
  case 8: 
    digitalWrite(row8, HIGH); 
    break;
  default: 
    break;
  }
}

void setup(){ 
  int i = 0 ; 
  for(i=2;i<18;i++) 
  { 
    pinMode(i, OUTPUT); 
  } 
  for(i=2;i<18;i++) { 
    digitalWrite(i, LOW); 
  } 
} 
void loop(){ 
  int t1;
  int l;
  //int arrage;
  //for(arrage=0;arrage<10;arrage++)
  //{
  for(l=0;l<8;l++)
  {
    for(t1=0;t1<8;t1++)
    {
      displayLed((l+1),(t1+1));
      delay(500);
    }
  }
  //}
} 





