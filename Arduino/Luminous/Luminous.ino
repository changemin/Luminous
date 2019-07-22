#include<Servo.h>

#define leftArmPin 14
#define leftFingerPin 16
#define rightArmPin 4
#define rightFingerPin 2
#define topbarPin 12

Servo leftArm, leftFinger, rightArm, rightFinger, topbar;

int value = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("[System] : Program Started");

  leftArm.attach(leftArmPin);
  leftFinger.attach(leftFingerPin);
  rightArm.attach(rightArmPin);
  rightFinger.attach(rightFingerPin);
  topbar.attach(topbarPin);
  servoReset();
}

int moveServo(Servo sv, int degree){
  sv.write(degree);
  delay(500);
  Serial.print("[moveServo] : Servo moved to ");
  Serial.println(degree);
}

int moveServoLong(Servo sv, int degree){
  sv.write(degree);
  delay(3000);
  Serial.print("[moveServo] : Servo moved to ");
  Serial.println(degree);
}

//void topbarRight(){
//  Serial.print("[moveServo] : Servo moved to ");
//  Serial.println(180);
//  topbar.attach(topbarPin);
//  topbar.write(180);
//  delay(3000);
//}
//
//void topbarLeft(){
//  Serial.print("[moveServo] : Servo moved to ");
//  Serial.println(00);
//  topbar.attach(topbarPin);
//  topbar.write(0);
//  delay(3000);
//}

void servoReset(){
  rightArm.write(120);
  rightFinger.write(0);
  topbar.write(180);
  moveServo(leftFinger, 90);
  moveServo(leftArm, 70);
  delay(1000);
}
void loop() {

  if(Serial.available() > 0){
    value = Serial.parseInt();
    if(value > 0){
      Serial.print("input ");
      moveServo(leftArm, 0);
      moveServo(leftFinger, 0); //책을 넘겼을 때 막히지 않도록 왼쪽 거치대를 잠시 치워준다.
    
      moveServo(rightArm, 40);
      moveServo(rightFinger, 180);

      moveServo(topbar, 0);
      moveServo(rightArm, 100);
      moveServo(rightFinger, 0);
      moveServo(topbar, 0);

      servoReset();
    
      value = 0;
    }
  }

}
