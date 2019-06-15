/*
Arduino code for just dispensing liquid.

This code is meant to actuate a single 12V solenoid valve.
Since the Arduino can only output a 5V signal, the Arduino will
require a connection to a 5V relay.  A 12V supply will be connected
to the ends of the relay to be switched on/off by the 5V signal.

TODO:
    Required:
    - DONE - Receive a serial signal to commnad valve actuation
    - DONE - Output 5V to relay board to open solenoid valve
    - DONE - Stop 5V output to close solenoid valve
    
    Optional:
    - Send serial signal indicating solenoid is open or closed
    - Use a 2nd relay to or low voltage LED to indicate valve status 
*/

#include <stdio.h>
#include <stdlib.h>

#define SOLENOID_RELAY 2

char character;
int charsAvailable;
String currentCommand, commandBuffer, serialInput;


void setup() {
    pinMode(SOLENOID_RELAY, OUTPUT);
    Serial.begin(9600);
}


void loop() {
    serialInput = serialDataRead();
    serialInput.remove(serialInput.indexOf('\r'));
    serialInput.remove(serialInput.indexOf('\n'));
    
    if (serialInput.indexOf("Open valve") > 0) {
        openSolenoid(SOLENOID_RELAY);
    }

    if (serialInput.indexOf("Close valve") > 0) {
        closeSolenoid(SOLENOID_RELAY);
    }
}


void openSolenoid(int controlPin) {
    digitalWrite(controlPin, HIGH);
    Serial.println("Valve open");
}


void closeSolenoid(int controlPin) {
    digitalWrite(controlPin, LOW);
    Serial.println("Valve closed");
}


String serialDataRead() {
    currentCommand = "";
    charsAvailable = Serial.available();
    if (charsAvailable > 0) {
        for (int i = 0; i < charsAvailable; i++) {
            character = Serial.read();
            if (character == '\n') {
                currentCommand = commandBuffer;
                commandBuffer = "";
            } else {
                commandBuffer.concat(character);
            }
        }
    }
    return currentCommand;
}
