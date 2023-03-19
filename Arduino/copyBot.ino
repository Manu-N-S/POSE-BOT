#include <Servo.h> 

Servo s1;
Servo s2;
Servo s3;
Servo s4;
Servo s5;
Servo s6;
Servo s7;
Servo s8;
        
int counter = 0;
bool counterStart = false;
String receivedString;

int lelbow=0;
int relbow=180;
int lshoulder=0;
int rshoulder=180;
int lhip=180;
int rhip=0;
int lknee=180;
int rknee=0;

void setup(){
  
  Serial.begin(9600);
  s1.attach(A0);
  s2.attach(A1);
  s3.attach(A2);
  s4.attach(A3);
  s5.attach(A4);
  s6.attach(A5);
  s7.attach(3);
  s8.attach(5);
}

void receieveData(){
  if(Serial.available()){
    
    while(Serial.available())
  {
    char c = Serial.read();

    if (c=='$'){
      counterStart = true;
    }
    if(counterStart)
      if(counter<=24)
      {
        receivedString = String(receivedString+c);
        counter++;
      }
      if(counter>24)
      {
        lshoulder = receivedString.substring(1,4).toInt();
        rshoulder = receivedString.substring(4,7).toInt();
        lelbow = receivedString.substring(7,10).toInt();
        relbow = receivedString.substring(10,13).toInt();
        lhip = receivedString.substring(13,16).toInt();
        rhip = receivedString.substring(16,19).toInt();
        lknee = receivedString.substring(19,22).toInt();
        rknee = receivedString.substring(22,25).toInt();
        receivedString ="";
        counter=0;
        counterStart = false;     
      }
  }
  }
}

void loop(){

  receieveData();
    Serial.print(lshoulder);
    Serial.print(" ");
    s1.write(lshoulder);

    Serial.print(rshoulder);
    Serial.print(" ");
    s2.write(rshoulder);
    
    Serial.print(lelbow);
    Serial.print(" ");
    s3.write(lelbow);

    Serial.print(relbow);
    Serial.print(" ");
    s4.write(relbow);

    Serial.print(lhip);
    Serial.print(" ");
    s5.write(lhip);

    Serial.print(rhip);
    Serial.print(" ");
    s6.write(rhip);

    Serial.print(lknee);
    Serial.print(" ");
    s7.write(lknee);

    Serial.print(rknee);
    Serial.print("\n");
    s8.write(rknee);

}
