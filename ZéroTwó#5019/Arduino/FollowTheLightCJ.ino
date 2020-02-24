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
  Serial.print("\n");
  Serial.print("==========");
  Serial.print("\n");
  Serial.print("X1:");
  Serial.print( analogRead(x1));
  Serial.print("\n");
  Serial.print("X2:");
  Serial.print( analogRead(x2));
  Serial.print("\n");
  Serial.print("Pos:");
  Serial.print( pos);
  Serial.print("\n");
  Serial.print("==========");
  Serial.print("\n");
  
  int x1diff = analogRead(x1) - defx1;
  int x2diff = analogRead(x2) - defx2;

  if ((x1diff > 10) || (x2diff > 10)){
    if((x1diff > x2diff) && (pos < 270)){
        pos = pos + 2;
        servoX.write(pos);
    }else if((x2diff > x1diff) && (pos > 0)){
        pos = pos - 2; 
        servoX.write(pos);
    }
  }
  delay(300);

}