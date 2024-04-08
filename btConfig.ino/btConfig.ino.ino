const int led = 13;
const int btPow = 12;


String btName = "btDev";
char pswd[5] = "0000";
char vBaud = "4";//AT command equivalent to 9600 baud
char mode = "1";//0 = slave, 1= master

void setup(){
  pinMode(led, OUTPUT);
  pinMode(btPow, OUTPUT);

  Serial.begin(38400);//AT config mode default baudrate

 //led indicator to press button --> AT mode entry
 digitalWrite(led, HIGH);
 delay(5000);
 digitalWrite(led, LOW);


 
 digitalWrite(btPow ,HIGH);
 delay(100);
 Serial.write("AT\r\t");//line endings to represent end of command
 Serial.print("AT+NAME:");
 Serial.print(btName);
 Serial.print("\r\t");

 Serial.print("AT+PIN:");//;or AT+PSWD
 Serial.print(pswd);
 Serial.print("\r\t");

 Serial.print("AT+BAUD:");
 Serial.print(vBaud);
 Serial.print("\r\t");

 Serial.print("AT+MODE");
 Serial.print(mode);
 Serial.print("\r\t");

 digitalWrite(led, HIGH);
 digitalWrite(btPow, LOW);
 delay(100);
 digitalWrite(btPow, HIGH);
}

void loop(){
  if(Serial.available()){
    Serial.write(Serial.read());
  }
}
