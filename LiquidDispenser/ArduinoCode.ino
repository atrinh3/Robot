/*
Arduino code for just dispensing liquid.

This code is meant to actuate a single 12V solenoid valve.
Since the Arduino can only output a 5V signal, the Arduino will
require a connection to a 5V relay.  A 12V supply will be connected
to the ends of the relay to be switched on/off by the 5V signal.

TODO 6/15:
    Required:
    - DONE - Receive a serial signal to commnad valve actuation
    - DONE - Output 5V to relay board to open solenoid valve
    - DONE - Stop 5V output to close solenoid valve
    
    Optional:
    - DONE - Send serial signal indicating solenoid is open or closed
    - DONE - Use a 2nd relay to or low voltage LED to indicate valve status 
*/

#include <stdio.h>
#include <stdlib.h>

#define SOLENOID_RELAY 2
#define SOLENOID_LED 3

#define TEST "Are you there"
#define TEST_REPLY "I am here"

char character;
int charsAvailable;
String currentCommand, commandBuffer, serialInput;


void setup() {
    pinMode(SOLENOID_RELAY, OUTPUT);
    pinMode(SOLENOID_LED, OUTPUT);
    Serial.begin(9600);
}


void loop() {
    serialInput = serialDataRead();
    serialInput.remove(serialInput.indexOf('\r'));
    serialInput.remove(serialInput.indexOf('\n'));
    
    if (serialInput.indexOf(TEST) > 0) {
        Serial.println(TEST_REPLY);
    } else if (serialInput.indexOf("Open valve") > 0) {
        openSolenoid(SOLENOID_RELAY);
        ledOn(SOLENOID_LED);
    } else if (serialInput.indexOf("Close valve") > 0) {
        closeSolenoid(SOLENOID_RELAY);
        ledOff(SOLENOID_LED);
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


void ledOn(int ledPin) {
    digitalWrite(ledPin, HIGH);
}


void ledOff(int ledPin) {
    digitalWrite(ledPin, LOW);
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
