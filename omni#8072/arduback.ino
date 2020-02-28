#include <Servo.h>
Servo servoX;

int pos = 0;

int x1 = A0;
int x2 = A2;



int defx1 = analogRead(x1);
int defx2 = analogRead(x2);

void setup() {
  servoX.attach(2);

  Serial.begin(9600); 

  
  

}


void loop() {
  
  int x1diff = analogRead(x1) - defx1;
  int x2diff = analogRead(x2) - defx2;

  if ((x1diff > 10) || (x2diff > 10)){
    if((x1diff > x2diff) && (pos < 180)){
        pos = pos + 2;
        servoX.write(pos);
    }else if((x2diff > x1diff) && (pos > 0)){
        pos = pos - 2; 
        servoX.write(pos);
    }
  }

  if (Serial.available() > 0) {
    String str = Serial.readString();
    
    if(str){
      if(str.startsWith("get")){
        Serial.print(pos);
      }
    }
  }

  delay(10);

}