#include <Servo.h>
#define LeftArmPin 3
#define LeftFingerPin 4
#define RightArmPin 5
#define RightFingerPin 6
#define TurnerPin 7

int value = 0;

Servo LeftArm, LeftFinger, RightArm, RightFinger, Turner; //서보모터 초기화

void setup() {
  Serial.begin(9600); //시리얼 포트 열기
  Serial.println("[Program Start]");
}

int moveServo(Servo sv, int pin, int degree)
{
  sv.attach(pin); //서보모터를 핀과 연결
  sv.write(degree); //사용자가 입력한 각도까지 서보모터 이동
  delay(1000);
  sv.detach(); //서보모터의 움직임이 모두 끝난 후, 연결을 끊어 준다.(끊임없이 입력한 각도로 움직이려 시도하기 때문에 모터가 떨리는 현상이 발생하게 됨.)
  Serial.print("[servo]moved to ");
  Serial.println(degree); //움직인 각도 출력
}

void loop() {
    if(Serial.available() > 0){
        value = Serial.parseInt(); //라즈베리파이로 부터 시리얼 데이터를 받는다
        if(value == 1){
          Serial.println(value); //받은 시리얼 데이터를 출력한다.
          moveServo(LeftArm, LeftArmPin, 0);
          moveServo(LeftFinger, LeftFingerPin, 0); //책을 넘겼을 때 막히지 않도록 왼쪽 거치대를 잠시 치워준다.
          
          moveServo(RightArm, RightArmPin, 20);
          moveServo(RightFinger, RightFingerPin, 150);
          moveServo(Turner, TurnerPin, 0); 
          
          moveServo(LeftFinger, LeftFingerPin, 90);
          moveServo(LeftArm, LeftArmPin, 90);
          
          delay(2000);
          moveServo(RightArm, RightArmPin, 60);
          moveServo(RightFinger, RightFingerPin, 0);
          moveServo(Turner, TurnerPin, 180);        
        }
   }
}
