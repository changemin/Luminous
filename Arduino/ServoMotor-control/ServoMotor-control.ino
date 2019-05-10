#include<Servo.h>
Servo servo;
int value = 0;
#define servoPin 5

void setup(){
  servo.attach(servoPin);
  Serial.begin(9600);
}

void loop(){
  if(Serial.available()){
    char in_data;
    in_data = Serial.read();
    if(in_data == '1'){
      value += 30;
      if(value == 180){
        value = 0;
      }
    }
    else{
      value = 0;
    }
    servo.write(value);
  }
}
