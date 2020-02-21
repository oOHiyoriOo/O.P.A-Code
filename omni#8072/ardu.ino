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
    }else if(str.startsWith("test")){ 
        myservo.write(0);
        delay(1000);
        myservo.write(45);
        delay(1000);
        myservo.write(90);
        delay(1000);
        myservo.write(135);
        delay(1000);
        myservo.write(180);
        delay(1000);
        myservo.write(0);

    }else if(str.startsWith("get")){ 

        str = myservo.read();
        Serial.print("at "+str+"°\n");

    

    }else if(str.startsWith("set")){
        str.replace("set","");
        int e = str.toInt();
        myservo.write(e);
    
      }
    
      }}

}