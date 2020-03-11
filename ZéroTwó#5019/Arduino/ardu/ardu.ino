
#include <pt.h>
#include <Servo.h>

Servo bot;
Servo top;

int pos = 0;

int x1 = A0;
int x2 = A2;

int defx1 = analogRead(x1);
int defx2 = analogRead(x2);

static struct pt pt1, pt2;


//Protothread: Get values
static int ptping(struct pt *pt){
  static unsigned long lastRead = 0;
  static String str, str2;
  PT_BEGIN(pt);
  while(1) {
    lastRead = millis();
    PT_WAIT_UNTIL(pt, millis() - lastRead > 1000);
    str = bot.read();
    str2 = top.read();
    Serial.print("bot:"+str+"\n");
    Serial.print("bot:"+str2+"\n");

  }
  PT_END(pt);
}

//Protothread: Set random (DEBUG)
static int randpos(struct pt *pt){
  static unsigned long lastSet = 0;
  
  static int x1diff, x2diff;
  PT_BEGIN(pt);
  while(1) {

    lastSet = millis();
    PT_WAIT_UNTIL(pt, millis() - lastSet > 5000);
    
    x1diff = analogRead(x1) - defx1;
    x2diff = analogRead(x2) - defx2;


    if ((x1diff > 10) || (x2diff > 10)){
      if((x1diff > x2diff) && (pos < 180)){
          pos = pos + 20;
          bot.write(pos);
          top.write(pos);
          Serial.print("Updated. \n");
    }else if((x2diff > x1diff) && (pos > 0)){
          pos = pos - 20; 
          bot.write(pos);
          top.write(pos);
          Serial.print("Updated. \n");
    }
    }
   
  }
  PT_END(pt);
}

void setup() {

  pinMode(LED_BUILTIN, OUTPUT);

  bot.attach(9);
  top.attach(11);
  Serial.begin(9600);
  //bot.write(0);
  //top.write(0);
  bot.write(90);
  top.write(90);
  PT_INIT(&pt1);
  PT_INIT(&pt2);
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
        Serial.print("1 at light level ");
        Serial.print(analogRead(x1));
        Serial.print(". \n");
        Serial.print("2 at light level ");
        Serial.print(analogRead(x2));
        Serial.print(". \n");
              
      }else if(str.startsWith("set")){
          str.replace("set","");
          int e = str.toInt();
          bot.write(e);
      
        }

    }else if(str.startsWith("1.")){
      //TOP SERVO
      
      str.replace("1.","");
      Serial.print("got input");
      
    }
                
    }
      }
    ptping(&pt1);
    randpos(&pt2);

}