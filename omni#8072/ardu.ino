#include <Servo.h>
Servo myservo;

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
  myservo.attach(9);
  Serial.begin(9600);
}



void loop() {

  while(Serial.available() > 0 ){
    String str = Serial.readString();
    
    if(str){
      if(str.startsWith("ping")){
        int i = 0;
        while (i < 3){
          digitalWrite(LED_BUILTIN, HIGH);
          delay(1000);
          digitalWrite(LED_BUILTIN, LOW);
          delay(1000);
          i++;
        }
        //TODO:: SIMPLIFY
    }else if(str.startsWith("r")){ 
        str.replace("r","");
        int e = str.toInt();
        myservo.write(0);
        delay(e);
        myservo.write(90);

    }else if(str.startsWith("l")){
        str.replace("l","");
        int e = str.toInt();
        myservo.write(180);
        delay(e);
        myservo.write(90);
    
      }
    
      }}

}
