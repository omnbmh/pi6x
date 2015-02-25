/*
* learn 01
* 这个例子要实现使用一个按键控制LED灯的亮灭 增加防抖
* Written by ChenDezhi in 2015 02 25 
* 参考 
* http://www.arduino.cn/thread-6327-1-1.html
* http://www.geek-workshop.com/thread-2874-1-1.html
* http://baike.baidu.com/link?url=l9VC8M6-pX4IQ6RxjDYKnWRel9eTjZjwg9g9jP_tlP2Uojfb-adLrYFW7DVNb-jgmRTyvK6xTEf9-suYlGiQDq
*/

#define LED_PIN 13
#define BUTTON_PIN 12
#define BUTTONS_SAMPLES 6000
#define BUTTON_PRESSED LOW

unsigned led_state = LOW;
unsigned int o_prell = 0;
boolean button_state = false;

void setup(){
  //Serial.begin(9600);
  
  pinMode(LED_PIN,OUTPUT);
  pinMode(BUTTON_PIN,INPUT_PULLUP);
  
  digitalWrite(LED_PIN,led_state);
}

void loop(){
  /*
  state = digitalRead(BUTTON_PIN);
  if(val == LOW){ //按键按下
    state = !state;
  }
  digitalWrite(LED_PIN,state);
  delay(1000);//延迟 消除杂波干扰
  */
  check_button();
  digitalWrite(LED_PIN,led_state);
}

void check_button(){
  int val = digitalRead(BUTTON_PIN);
  if((val == BUTTON_PRESSED) && (o_prell < BUTTONS_SAMPLES)){
    //Serial.println("1");
    o_prell = o_prell+1;
  }
  else if((val == BUTTON_PRESSED) && (o_prell >= BUTTONS_SAMPLES) && (!button_state)){
    //Serial.println("2");
    button_state = true;
    led_state = !led_state;
  }
  else if((val != BUTTON_PRESSED) && (o_prell > 0)){
    //Serial.println("3");
    o_prell = o_prell-1;
  }
  else if((val != BUTTON_PRESSED) && (o_prell <= 0) && button_state){
    //Serial.println("4");
    button_state = false;
  }
  /*
  Serial.print("button val ");
  Serial.print(val);
  Serial.println(";");
  
   Serial.print("button o_prell ");
  Serial.print(o_prell);
  Serial.println(";");
  
  Serial.print("button state ");
  Serial.print(button_state);
  Serial.println(";");
  
  Serial.print("led state ");
  Serial.print(led_state);
  Serial.println(";");
  //delay(100);
  */
}
