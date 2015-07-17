//Team Sailing Research 
//This Arduino code was written in the summer of 2014 as part of the first prototype system for Team Sailing Research. We used a Velleman 12 Key keypad, along with an Arduino
//Uno, an XBee Radio Shield for the Arduino Uno, and a custom PCB for our MCP23017 port expander. We set up the keypad so that each key, 1-9 and Hash, all are written out
//to the Raspberry Pi part of our system through the XBee. We also increased the amount of keys we have by using the Star Key as a tab, so that holding down the Star Key while
//presseing another key can be recognized as a different key press.

#include "Wire.h"     // Use the Wire Library for I2C
#include <SoftwareSerial.h>  // Used to write and read from the XBees

SoftwareSerial XBee(2, 3);  //Sets which RX and TX Pins the XBee is connected to
byte a=0;             // Variable to store the byte from Port A of the MCP23017 in
byte b=0;            // Variable to store the byte from Port B 
byte lastsig_a = 0;    //Way to check what last byte was, used to make sure that even if button is held down, RPi only reads one key press
byte lastsig_b = 0;    //same purpose as above but for Port B

void setup()
{
   Serial.begin(9600);  //used for debugging purposes to look at the Arduino's serial monitor
  XBee.begin(9600);  // begins XBee communication, baud rate of 9600 
  pinMode(2, INPUT);  //found in a tutorial to get the Arduino to write to an XBee, sets the RX Pin as input
  pinMode(3, OUTPUT);  //sets the TX Pin as output
  Wire.begin();                 // wake up I2C bus
  Wire.beginTransmission(0x20); // Connect to chip
  
  //Bank A is set to inputs by default so we don't need to write anything special to it
  Wire.write((byte)0x01);       // Select Bank B
  Wire.write((byte)0xF);       // Set four pins of Bank B as inputs, the rest as outputs, with our custom PCB shield, this isn't particularly necessary but keep it just in case you actually need ouputs for some reason
  Wire.endTransmission();       // Close connection
}
 
void loop()
{
  // Read the inputs of bank A
  Wire.beginTransmission(0x20); // Connect to chip
  Wire.write(0x12);             // Set Memory Pointer to Bank A
  Wire.endTransmission();       // Close connection
  Wire.requestFrom(0x20, 1);    // Request one byte
  a=Wire.read();                // Put the Byte into variable 'a'
  Serial.println(a);          // Used for debugging, let's you see what keys have been pressed on Port A, which are 1, 2, 4, 5, 7, 8, Star, and 0
  
  // Read the first four pins of Bank B
  Wire.beginTransmission(0x20);  // Connect to chip
  Wire.write(0x13);              // Set Memory Pointer to Bank B
  Wire.endTransmission();        // Close connection
  Wire.requestFrom(0x20, 1);     // Request one byte
  b = Wire.read();               // Put the Byte into variable 'b'
  Serial.println(b);           // Used for debugging, let's you see what keys have been pressed on Port B, which are 3, 6, 9, and Hash
  
  if (a != lastsig_a || a == 1){  // checks to see if our current byte is different from our last one, used to make sure that holding down a key doesn't produce multiple readings, but also evaluates to True if the Star Key is being held down
    lastsig_a = a;      // sets the current signal to the last signal, on next loop, will check to see if they are different
    
    if (b != lastsig_b){  //Assuming above if statement evaluated to True because the Star Key was pressed, we check to see if any key has been pressed on Port B and then we write out the Star Key and whichever Port B key has been pressed
      lastsig_b = b;
      
      if (b == 1){
        XBee.println("Star Key & Hash Key");
        Serial.println("Star Key & Hash Key");
      }
      else if (b == 2){
        XBee.println("Star Key & 9 Key");
        Serial.println("Star Key & 9 Key");
      }
      else if (b == 4){
        XBee.println("Star Key & 6 Key");
        Serial.println("Star Key & 6 Key");
      }
      else if (b == 8){
        XBee.println("Star Key & 3 Key");
        Serial.println("Star Key & 3 Key");
      }
    }
    //else we assume that no key on Port B has been pressed and we proceed to check only Port A
    else if (a == 2){    // These are the binary values when pin 3 of the Velleman 12 key is connected to the first GPIO pin of Port A on MCP23017
      XBee.println("7 Key");  //We identify which key has been pressed based on the binary values and commmunicate them to the RPi over XBee radios
      Serial.println("7 Key");  //The Serial.println statements are for debugging, uncomment them to see what the Arduino is reading and printing
    }
    else if (a == 3){  //The odd binary values are due to when the Star Key and another key on Port A has been pressed
      XBee.println("Star Key & 7 Key");  //So we do the same thing as we did in the above else if statement, except we write out Star Key with whichever key has been pressed
      Serial.println("Star Key & 7 Key");
    }
    else if (a == 4){
      XBee.println("4 Key");
      Serial.println("4 Key");
    }
    else if (a == 5){
      XBee.println("Star Key & 4 Key");
      Serial.println("Star Key & 4 Key");
    }
    else if (a == 8){
      XBee.println("1 Key");
      Serial.println("1 Key");
    }
    else if (a == 9){
      XBee.println("Star Key & 1 Key");
      Serial.println("Star Key & 1 Key");
    }
    else if (a == 16){
      XBee.println("0 Key");
      Serial.println("0 Key");
    }
    else if (a == 17){
      XBee.println("Star Key & 0 Key");
      Serial.println("Star Key & 0 Key");
    }
    else if (a == 32){
      XBee.println("8 Key");
      Serial.println("8 Key");
    }
    else if (a == 33){
      XBee.println("Star Key & 8 Key");
      Serial.println("Star Key & 8 Key");
    }
    else if (a == 64){
      XBee.println("5 Key");
      Serial.println("5 Key");
    }
    else if (a == 65){
      XBee.println("Star Key & 5 Key");
      Serial.println("Star Key & 5 Key");
    }
    else if (a == 128){
      XBee.println("2 Key");
      Serial.println("2 Key");
    }
    else if (a == 129){
      XBee.println("Star Key & 2 Key");
      Serial.println("Star Key & 2 Key");
    }

  }
 
 if (b != lastsig_b){  // The Velleman 12 key has 12 analog outpts but the Port A of the MCP23017 has 8 GPIO pins, need to use 4 on Port B
   lastsig_b = b;    // Same thing as Port A except the byte readings, which are the same numbers, correspond to different keys on Port B

   if (b == 1){
      XBee.println("Hash Key");
      Serial.println("Hash Key");
    }
   else if (b == 2){
     XBee.println("9 Key");
     Serial.println("9 Key");
   }
   else if (b == 4){
     XBee.println("6 Key");
     Serial.println("6 Key");
   }
   else if (b == 8){
     XBee.println("3 Key");
     Serial.println("3 Key");
   }
   
 } 
  
  delay(75);                 // Small delay to debounce switch
}
