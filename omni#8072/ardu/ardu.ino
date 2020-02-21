#include <Servo.h>
Servo bot;
//Servo top;

int pos = 0;


void setup() {

//   pinMode(0, OUTPUT);
//   pinMode(1, OUTPUT);
//   pinMode(2, OUTPUT);
  
//   pinMode(3, OUTPUT);
//   pinMode(4, OUTPUT);
//   pinMode(5, OUTPUT);
  
//   pinMode(6, OUTPUT);

  pinMode(LED_BUILTIN, OUTPUT);

  // 
  bot.attach(9);
  //top.attach(3);                                                    servo top stage
  Serial.begin(9600);
  bot.write(0);
  //top.write(0);
}



void loop() {

  while(Serial.available() > 0 ){
    String str = Serial.readString();
    
    if(str){

    if(str.startsWith("0.")){
      //BOT SERVO
      str.replace("0.","");

      if(str.startsWith("test")){ 
        bot.write(0);
        delay(1000);
        bot.write(45);
        delay(1000);
        bot.write(90);
        delay(1000);
        bot.write(135);
        delay(1000);
        bot.write(180);
        delay(1000);
        bot.write(0);
            
      }else if(str.startsWith("get")){ 
            
        str = bot.read();
        Serial.print("at "+str+"°\n");
              
      }else if(str.startsWith("set")){
          str.replace("set","");
          int e = str.toInt();
          bot.write(e);
      
        }

    }else if(str.startsWith("1.")){
      //TOP SERVO

      
      str.replace("1.","");
      
      
    }
                
    
    }
      }

}