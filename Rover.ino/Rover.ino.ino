#include<SoftwareSerial.h>

SoftwareSerial btDev(8,9);//create a device instance(btDev)--> NOTE(1arg: RX, 2arg:TX)
char c; 
void setup(){
  
  pinMode(10,OUTPUT);//key/en pin
  digitalWrite(10,HIGH);

  Serial.begin(9600);//default board baudrate
  btDev.begin(9600);//default chipset baudrate for AT config 
  Serial.print("Enter AT commands: ");


}

void loop(){
    
  if(Serial.available())
    btDev.write(Serial.read());

  if(btDev.available())
    Serial.print(btDev.read());
  
}
