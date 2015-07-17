#include "Wire.h"

void setup() {                
  Wire.begin();//wake up I2C busj
  Wire.beginTransmission(0x20);
  Wire.write(0x00); //I0DIRA register
  Wire.write(0x00); //set all of port A to output
  Wire.endTransmission();
  Wire.beginTransmission(0x20);
  Wire.write(0x01); //I0DIRA register
  Wire.write(0x00); //set all of port B to output
  Wire.endTransmission();
}

void binaryCount(){
 for (byte a=0; a<256; a++){
 Wire.beginTransmission(0x20);
 Wire.write(0x12); // GPIOA
 Wire.write(a); // port A
 Wire.endTransmission();
 Wire.beginTransmission(0x20);
 Wire.write(0x13); // GPIOB
 Wire.write(a); // port B
 Wire.endTransmission();
 }
}

void loop(){
 binaryCount();
 delay(500);
}
